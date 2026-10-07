import re

with open("app/templates/index.html", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find('<div id="badge-showcase-section"')
idx_manifesto = text.find('<!-- ETHICAL ADVERTISING & ZERO-MOCK MANIFESTO -->')
idx_end = text.rfind('</div>', idx_start, idx_manifesto) + 6

streamlined_stage = """      <!-- ===================================================================== -->
      <!-- UNIFIED INTERACTIVE BADGE STAGE (DECLUTTERED 2026 UX)                 -->
      <!-- ===================================================================== -->
      <div id="badge-showcase-section" class="pt-8 space-y-6 border-t border-gray-800">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-[11px] font-semibold uppercase tracking-wider mb-2">
              <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
              <span>Interactive Badge Suite</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Dynamic Badge Styles &amp; Live Studio
            </h2>
            <p class="text-gray-400 text-sm mt-1 max-w-2xl">
              Preview all 7 layout formats, 9 themes, and live SVG vectors instantly. Unlock the Live Badge Studio by claiming your repository.
            </p>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="loginWithGitHubForDashboard()" class="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-bold text-xs shadow-lg transition flex items-center space-x-1.5">
              <i data-lucide="lock" class="w-3.5 h-3.5"></i>
              <span>Unlock Live Badge Studio</span>
            </button>
          </div>
        </div>

        <!-- THE UNIFIED INTERACTIVE STAGE CARD -->
        <div class="glass-panel rounded-2xl p-5 sm:p-7 space-y-5 border-gray-800 shadow-2xl glow-emerald">
          <!-- 7-Style Segmented Bar -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-800 pb-4">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-gray-400">Selected Style:</span>
              <span id="gallery-style-label" class="text-xs font-bold text-brand-300 ml-1.5 font-mono">Glass Banner (500x110)</span>
            </div>

            <!-- Segmented Layout Buttons -->
            <div class="flex items-center space-x-1 overflow-x-auto pb-1 sm:pb-0 text-xs font-medium">
              <button onclick="selectGalleryStyle('banner')" id="gtab-banner" class="px-2.5 py-1.5 rounded-lg bg-brand-500/20 text-brand-300 border border-brand-500/30 transition">Banner</button>
              <button onclick="selectGalleryStyle('linear')" id="gtab-linear" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Linear</button>
              <button onclick="selectGalleryStyle('spotlight')" id="gtab-spotlight" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Spotlight</button>
              <button onclick="selectGalleryStyle('compact')" id="gtab-compact" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Compact</button>
              <button onclick="selectGalleryStyle('backer')" id="gtab-backer" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Backer</button>
              <button onclick="selectGalleryStyle('goal')" id="gtab-goal" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Goal</button>
              <button onclick="selectGalleryStyle('shield')" id="gtab-shield" class="px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition">Shield.io</button>
            </div>
          </div>

          <!-- Live Stage Viewport -->
          <div class="p-6 bg-gray-950/90 rounded-xl border border-gray-800/80 flex items-center justify-center min-h-[140px] overflow-x-auto shadow-inner">
            <img id="gallery-stage-img" src="/badge/tiangolo/fastapi.svg?style=banner&theme=dark" alt="Badge Preview" class="max-w-full h-auto rounded shadow-xl transition-all duration-300">
          </div>

          <!-- Controls: Theme, Marquee & 1-Click Copy -->
          <div class="flex flex-wrap items-center justify-between gap-3 text-xs pt-1">
            <div class="flex items-center space-x-3 flex-wrap gap-y-2">
              <div class="flex items-center space-x-1.5">
                <span class="text-gray-400 font-semibold">Theme:</span>
                <select id="gallery-theme-sel" onchange="refreshGalleryStage()" class="bg-gray-900 border border-gray-700 rounded-lg px-2.5 py-1 text-xs text-white focus:outline-none focus:border-brand-500">
                  <option value="dark">Dark Slate</option>
                  <option value="cyberpunk">Cyberpunk Neon</option>
                  <option value="emerald">Emerald</option>
                  <option value="linear">Linear Monochrome</option>
                  <option value="dracula">Dracula</option>
                  <option value="nord">Nord</option>
                  <option value="monokai">Monokai</option>
                  <option value="synthwave">Synthwave</option>
                  <option value="light">Crisp Light</option>
                </select>
              </div>

              <label class="flex items-center space-x-1.5 cursor-pointer text-gray-300 hover:text-white">
                <input type="checkbox" id="gallery-chk-marquee" onchange="refreshGalleryStage()" class="rounded border-gray-700 text-brand-500 focus:ring-brand-500">
                <span class="font-medium">Marquee Ticker</span>
              </label>

              <label class="flex items-center space-x-1.5 cursor-pointer text-gray-400 hover:text-white">
                <input type="checkbox" id="gallery-chk-stars" onchange="refreshGalleryStage()" class="rounded border-gray-700 text-brand-500 focus:ring-brand-500">
                <span>Hide Stars</span>
              </label>
            </div>

            <div class="flex items-center space-x-2">
              <button onclick="copyGalleryMarkdown()" id="btn-gallery-copy" class="px-4 py-2 rounded-lg bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white font-bold text-xs shadow-lg transition flex items-center space-x-1.5">
                <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                <span id="gallery-copy-lbl">Copy README Markdown</span>
              </button>
              <button onclick="openMaintainerStudio(activeGalleryStyle, document.getElementById('gallery-theme-sel').value)" class="px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white border border-gray-700 text-xs font-semibold transition flex items-center space-x-1">
                <i data-lucide="sliders" class="w-3.5 h-3.5 text-brand-400"></i>
                <span>Open in Studio</span>
              </button>
            </div>
          </div>
        </div>

        <!-- COLLAPSIBLE ACCORDION FOR TECHNICAL URL PARAMETERS (Preserves docs, kills clutter) -->
        <div class="glass-panel rounded-xl border border-gray-800 overflow-hidden">
          <button onclick="toggleParamAccordion()" class="w-full p-4 text-left flex items-center justify-between text-xs font-bold text-gray-300 hover:text-white transition">
            <div class="flex items-center space-x-2">
              <i data-lucide="code" class="w-4 h-4 text-accent-400"></i>
              <span>Advanced README URL Parameters &amp; Query Syntax (Collapsible Cheatsheet)</span>
            </div>
            <i id="icon-param-accordion" data-lucide="chevron-down" class="w-4 h-4 text-gray-400 transition transform"></i>
          </button>
          
          <div id="param-accordion-content" class="hidden p-4 pt-0 border-t border-gray-800/60 overflow-x-auto text-xs">
            <table class="w-full text-left text-xs mt-3">
              <thead class="bg-gray-900 text-gray-400 uppercase font-semibold border-b border-gray-800">
                <tr>
                  <th class="px-3 py-2">Param</th>
                  <th class="px-3 py-2">Options</th>
                  <th class="px-3 py-2">Default</th>
                  <th class="px-3 py-2">Description</th>
                  <th class="px-3 py-2">Example</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800 text-gray-300">
                <tr>
                  <td class="px-3 py-2 font-mono text-brand-300">style</td>
                  <td class="px-3 py-2 font-mono text-gray-400">banner, linear, spotlight, compact, backer, goal, shield</td>
                  <td class="px-3 py-2 font-mono text-gray-400">banner</td>
                  <td class="px-3 py-2">Selects 1 of 7 visual layout styles.</td>
                  <td class="px-3 py-2 font-mono text-gray-400">?style=linear</td>
                </tr>
                <tr>
                  <td class="px-3 py-2 font-mono text-accent-300">theme</td>
                  <td class="px-3 py-2 font-mono text-gray-400">dark, cyberpunk, emerald, linear, dracula, nord, monokai, synthwave, light</td>
                  <td class="px-3 py-2 font-mono text-gray-400">dark</td>
                  <td class="px-3 py-2">Switches color palette.</td>
                  <td class="px-3 py-2 font-mono text-gray-400">?theme=dracula</td>
                </tr>
                <tr>
                  <td class="px-3 py-2 font-mono text-pink-300">marquee</td>
                  <td class="px-3 py-2 font-mono text-gray-400">true, false</td>
                  <td class="px-3 py-2 font-mono text-gray-400">false</td>
                  <td class="px-3 py-2">Continuous smooth right-to-left scrolling ticker.</td>
                  <td class="px-3 py-2 font-mono text-gray-400">?marquee=true</td>
                </tr>
                <tr>
                  <td class="px-3 py-2 font-mono text-purple-300">hide_stars</td>
                  <td class="px-3 py-2 font-mono text-gray-400">true, false</td>
                  <td class="px-3 py-2 font-mono text-gray-400">false</td>
                  <td class="px-3 py-2">Suppresses star badge count.</td>
                  <td class="px-3 py-2 font-mono text-gray-400">?hide_stars=true</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>"""

new_text = text[:idx_start] + streamlined_stage + text[idx_end:]

js_code = """
    // Streamlined Gallery Stage Controller
    let activeGalleryStyle = 'banner';
    const galleryStyleNames = {
      banner: 'Glass Hero Banner (500x110)',
      linear: 'Neo-Brutalist Linear Dark (500x110)',
      spotlight: 'Dual-Pill Radial Spotlight (500x110)',
      compact: 'Compact Minimal Strip (500x40)',
      backer: 'Supporter Backer Pill (320x28)',
      goal: 'Monthly Funding Goal Tracker (300x28)',
      shield: 'Shields.io Single-Line Marquee (520x28)'
    };

    function selectGalleryStyle(style) {
      activeGalleryStyle = style;
      const allStyles = ['banner', 'linear', 'spotlight', 'compact', 'backer', 'goal', 'shield'];
      allStyles.forEach(s => {
        const btn = document.getElementById(`gtab-${s}`);
        if (btn) {
          if (s === style) {
            btn.className = 'px-2.5 py-1.5 rounded-lg bg-brand-500/20 text-brand-300 border border-brand-500/30 transition';
          } else {
            btn.className = 'px-2.5 py-1.5 rounded-lg bg-gray-900 text-gray-400 hover:text-white border border-gray-800 transition';
          }
        }
      });
      const lbl = document.getElementById('gallery-style-label');
      if (lbl) lbl.innerText = galleryStyleNames[style] || style;
      refreshGalleryStage();
    }

    function refreshGalleryStage() {
      const img = document.getElementById('gallery-stage-img');
      if (!img) return;
      const theme = document.getElementById('gallery-theme-sel')?.value || 'dark';
      const marquee = document.getElementById('gallery-chk-marquee')?.checked;
      const hideStars = document.getElementById('gallery-chk-stars')?.checked;

      let q = [];
      if (activeGalleryStyle && activeGalleryStyle !== 'banner') q.push(`style=${activeGalleryStyle}`);
      if (theme && theme !== 'dark') q.push(`theme=${theme}`);
      if (marquee) q.push(`marquee=true`);
      if (hideStars) q.push(`hide_stars=true`);

      const queryStr = q.length > 0 ? `?${q.join('&')}` : '';
      img.src = `/badge/tiangolo/fastapi.svg${queryStr}`;
    }

    function copyGalleryMarkdown() {
      const theme = document.getElementById('gallery-theme-sel')?.value || 'dark';
      const marquee = document.getElementById('gallery-chk-marquee')?.checked;
      const hideStars = document.getElementById('gallery-chk-stars')?.checked;

      let q = [];
      if (activeGalleryStyle && activeGalleryStyle !== 'banner') q.push(`style=${activeGalleryStyle}`);
      if (theme && theme !== 'dark') q.push(`theme=${theme}`);
      if (marquee) q.push(`marquee=true`);
      if (hideStars) q.push(`hide_stars=true`);

      const queryStr = q.length > 0 ? `?${q.join('&')}` : '';
      const base = window.location.origin;
      const badgeUrl = `${base}/badge/tiangolo/fastapi.svg${queryStr}`;
      const clickUrl = `${base}/click/active/1`;
      const md = `[![Sponsorship Badge](${badgeUrl})](${clickUrl})`;

      navigator.clipboard.writeText(md).then(() => {
        const lbl = document.getElementById('gallery-copy-lbl');
        if (lbl) lbl.innerText = 'Copied to Clipboard!';
        setTimeout(() => { if (lbl) lbl.innerText = 'Copy README Markdown'; }, 2000);
        showToast('Copied badge Markdown snippet!');
      });
    }

    function toggleParamAccordion() {
      const content = document.getElementById('param-accordion-content');
      const icon = document.getElementById('icon-param-accordion');
      if (!content) return;
      content.classList.toggle('hidden');
      if (icon) {
        icon.classList.toggle('rotate-180');
      }
      updateIcons();
    }
"""

idx_script_end = new_text.rfind('</script>')
new_text = new_text[:idx_script_end] + js_code + new_text[idx_script_end:]

with open("app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Landing page successfully decluttered and modernized!")
