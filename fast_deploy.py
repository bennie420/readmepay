import base64
import tarfile
import io
import subprocess
import os

files = [
    "app/main.py",
    "app/routers/auth.py",
    "app/routers/badge.py",
    "app/routers/inventory.py",
    "app/routers/maintainers.py",
    "app/routers/sponsor_auth.py",
    "app/schemas/repo.py",
    "app/services/badge_service.py",
    "app/templates/badge.svg.j2",
    "app/templates/badge_linear.svg.j2",
    "app/templates/badge_spotlight.svg.j2",
    "app/templates/badge_compact.svg.j2",
    "app/templates/badge_backer.svg.j2",
    "app/templates/badge_goal.svg.j2",
    "app/templates/shield.svg.j2",
    "app/templates/index.html",
    "start.py",
    "README.md",
    "PROJECT.md",
    "docs/API.md",
    "docs/BADGES.md",
    "docs/ARCHITECTURE.md",
]

# Create an in-memory tar archive of all modified files
tar_stream = io.BytesIO()
with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
    for rel_path in files:
        if os.path.exists(rel_path):
            tar.add(rel_path, arcname=rel_path)

tar_stream.seek(0)
b64_tar = base64.b64encode(tar_stream.read()).decode("ascii")

# Shell script that unpacks tar in /opt/opensponsor and updates container in ONE shot
script = f"""
echo '{b64_tar}' | base64 -d | tar -xzf - -C /opt/opensponsor/
docker cp /opt/opensponsor/app/. opensponsor_app:/app/app/

# Purge any fake/unregistered seeded sponsor ads from database (host and docker container)
python3 -c "
import sqlite3
for db in ['/var/lib/docker/volumes/opensponsor_db_data/_data/badge_platform.db', '/opt/opensponsor/badge_platform.db']:
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        fake = ('Sentry', 'Neon', 'Supabase', 'Docker', 'GitHub Sponsors', 'PostHog')
        cur.execute('DELETE FROM ads WHERE sponsor_name IN (?, ?, ?, ?, ?, ?)', fake)
        cnt = cur.rowcount
        cur.execute('DELETE FROM impressions WHERE ad_id NOT IN (SELECT id FROM ads)')
        cur.execute('DELETE FROM clicks WHERE ad_id NOT IN (SELECT id FROM ads)')
        conn.commit()
        conn.close()
        print(f'Purged {{cnt}} fake sample ads from {{db}}')
    except Exception as e:
        print(f'Purge info {{db}}: {{e}}')
"

docker exec opensponsor_app python3 -c "
import sqlite3
for db in ['/data/badge_platform.db', '/app/badge_platform.db']:
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        fake = ('Sentry', 'Neon', 'Supabase', 'Docker', 'GitHub Sponsors', 'PostHog')
        cur.execute('DELETE FROM ads WHERE sponsor_name IN (?, ?, ?, ?, ?, ?)', fake)
        cnt = cur.rowcount
        cur.execute('DELETE FROM impressions WHERE ad_id NOT IN (SELECT id FROM ads)')
        cur.execute('DELETE FROM clicks WHERE ad_id NOT IN (SELECT id FROM ads)')
        conn.commit()
        cur.execute('SELECT id, sponsor_name FROM ads')
        print(f'Purged {{cnt}} fake ads from container {{db}}. Remaining: {{cur.fetchall()}}')
        conn.close()
    except Exception as e:
        print(f'Container purge info {{db}}: {{e}}')
"

docker restart opensponsor_app
docker restart opensponsor_caddy
"""

with open("batch_deploy.sh", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Executing one-shot batch deployment to Azure VM...")
res = subprocess.run([
    "az.cmd", "vm", "run-command", "invoke",
    "--resource-group", "rg-opensponsor-prod",
    "--name", "vm-opensponsor",
    "--command-id", "RunShellScript",
    "--scripts", "@batch_deploy.sh"
], capture_output=True, text=True)

print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
