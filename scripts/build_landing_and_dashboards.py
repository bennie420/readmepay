"""
Script to build the updated index.html with:
1. True SaaS Landing Page on tab-home (Hero, sells copy, mission statement, 2-sided marketplace, full Badge Styles & Options Gallery, 9 themes swatches, cheatsheet).
2. Badge Studio & Snippet Generator locked behind repo owner login in tab-revenue (Maintainer Dashboard).
3. First-class Sponsor Dashboard & Visual Login on tab-sponsors (Sponsor sign-in, brand selector, live ad preview, campaign management, deposits).
"""

import sys
from pathlib import Path

content = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ReadmePay &mdash; Economic Empowerment Infrastructure for Independent Open-Source Developers</title>
  <meta name="description" content="Economic empowerment infrastructure for independent open-source developers. Transparent 50/50 revenue sharing, dynamic README badges, language-targeted sponsor campaigns, and automated global payouts.">
  <link rel="icon" type="image/svg+xml" href="/favicon.ico">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
            },
            accent: {
              400: '#38bdf8',
              500: '#0ea5e9',
              600: '#0284c7',
            },
            dark: {
              900: '#0b0f19',
              800: '#111827',
              700: '#1f2937',
              600: '#374151',
            }
          },
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
            mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {
      font-family: 'Inter', sans-serif;
      background-color: #0b0f19;
      color: #f3f4f6;
    }
    .glass-panel {
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-card {
      background: rgba(31, 41, 55, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.06);
      transition: all 0.2s ease-in-out;
    }
    .glass-card:hover {
      border-color: rgba(16, 185, 129, 0.3);
      transform: translateY(-2px);
    }
    .glow-emerald {
      box-shadow: 0 0 25px -5px rgba(16, 185, 129, 0.2);
    }
    .tab-active {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(14, 165, 233, 0.15));
      border-color: #10b981;
      color: #34d399;
    }
    pre, code {
      font-family: 'JetBrains Mono', monospace;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-brand-500 selection:text-white">

  <!-- TOP NAVIGATION BAR -->
  <header class="sticky top-0 z-50 glass-panel border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3 cursor-pointer" onclick="switchTab('home')">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-accent-500 flex items-center justify-center shadow-lg shadow-brand-500/20">
          <i data-lucide="shield-check" class="w-6 h-6 text-white"></i>
        </div>
        <div>
          <span class="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-brand-400 via-teal-300 to-accent-400">
            ReadmePay
          </span>
          <span class="hidden sm:inline-block ml-2 text-xs uppercase px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-semibold tracking-wide">
            Live Platform
          </span>
        </div>
      </div>

      <!-- Nav Tabs -->
      <nav class="hidden md:flex items-center space-x-1">
        <button onclick="switchTab('home')" id="nav-home" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/60 transition flex items-center space-x-1.5 tab-active">
          <i data-lucide="home" class="w-4 h-4"></i>
          <span>Home</span>
        </button>
        <button onclick="scrollToGallery()" id="nav-gallery" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/60 transition flex items-center space-x-1.5">
          <i data-lucide="sparkles" class="w-4 h-4 text-emerald-400"></i>
          <span>Badge Gallery</span>
        </button>
        <button onclick="switchTab('revenue')" id="nav-revenue" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/60 transition flex items-center space-x-1.5">
          <i data-lucide="layout-dashboard" class="w-4 h-4 text-brand-400"></i>
          <span>Repo Owner Dashboard</span>
        </button>
        <button onclick="switchTab('sponsors')" id="nav-sponsors" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/60 transition flex items-center space-x-1.5">
          <i data-lucide="megaphone" class="w-4 h-4 text-accent-400"></i>
          <span>Sponsor Portal</span>
        </button>
        <button onclick="switchTab('directory')" id="nav-directory" class="nav-btn px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/60 transition flex items-center space-x-1.5">
          <i data-lucide="folder-git-2" class="w-4 h-4"></i>
          <span>Repository Index</span>
        </button>
      </nav>

      <!-- Right CTAs -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- Maintainer Auth Status Button -->
        <div id="nav-maintainer-cta">
          <button onclick="switchTab('revenue')" class="px-3 py-1.5 rounded-lg bg-[#24292f] hover:bg-[#1b1f23] text-xs font-semibold text-white border border-gray-700 transition flex items-center space-x-1.5 shadow-sm">
            <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            <span id="nav-user-label">Maintainer Login</span>
          </button>
        </div>

        <!-- Sponsor Auth Status Button -->
        <div id="nav-sponsor-cta">
          <button onclick="switchTab('sponsors')" class="px-3 py-1.5 rounded-lg bg-accent-500/15 hover:bg-accent-500/25 text-accent-300 border border-accent-500/30 text-xs font-semibold transition flex items-center space-x-1.5">
            <i data-lucide="megaphone" class="w-3.5 h-3.5 text-accent-400"></i>
            <span id="nav-sponsor-label">Sponsor Portal</span>
          </button>
        </div>

        <a href="/docs" target="_blank" class="hidden sm:flex px-2.5 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-semibold text-gray-300 hover:text-white border border-gray-700 transition items-center space-x-1">
          <i data-lucide="book-open" class="w-3.5 h-3.5"></i>
          <span>Docs</span>
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- ========================================================================= -->
    <!-- TAB 1: LANDING PAGE (HERO, SELLS COPY, 2-SIDED MARKET, FULL GALLERY)      -->
    <!-- ========================================================================= -->
    <section id="tab-home" class="tab-content space-y-12">
      <!-- HERO SECTION -->
      <div class="text-center max-w-4xl mx-auto pt-6 pb-2 space-y-5">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold uppercase tracking-wider">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          <span>Economic Empowerment Infrastructure for Independent Open-Source Developers</span>
        </div>
        
        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-tight">
          Turn Public README Traffic Into <span class="bg-clip-text text-transparent bg-gradient-to-r from-brand-400 via-emerald-300 to-accent-400">Dependable Monthly Income</span>
        </h1>
        
        <p class="text-gray-300 text-base sm:text-xl max-w-3xl mx-auto leading-relaxed">
          Open-source software powers 97% of modern systems, but independent developers carry the burden for free. ReadmePay compiles live GitHub metadata into dynamic badges, matches tech sponsorships to your language ecosystem, splits revenue 50/50 transparently, and sends automated monthly payouts to your PayPal or crypto wallet.
        </p>

        <!-- Primary Dual CTAs -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-3">
          <button onclick="loginWithGitHubForDashboard()" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white font-bold text-sm shadow-xl shadow-brand-600/30 transition flex items-center justify-center space-x-2.5">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            <span>Claim &amp; Monetize Repos (GitHub Sign In)</span>
          </button>
          <button onclick="switchTab('sponsors')" class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gray-900 hover:bg-gray-800 text-accent-300 hover:text-white border border-accent-500/40 font-bold text-sm shadow-lg transition flex items-center justify-center space-x-2">
            <i data-lucide="megaphone" class="w-4 h-4 text-accent-400"></i>
            <span>Sponsor Open-Source (Advertiser Hub)</span>
          </button>
        </div>

        <div class="pt-2 text-xs text-gray-500 flex flex-wrap items-center justify-center gap-4">
          <span class="flex items-center space-x-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-400"></i><span>Zero-Mock Live GitHub REST Data</span></span>
          <span class="flex items-center space-x-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-400"></i><span>Transparent 50/50 Revenue Split</span></span>
          <span class="flex items-center space-x-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-400"></i><span>Automated PayPal &amp; Crypto Payouts</span></span>
        </div>
      </div>

      <!-- TRACTION & PRINCIPLES COUNTER -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="glass-card rounded-2xl p-5 text-center space-y-1 border-brand-500/20">
          <div class="text-3xl sm:text-4xl font-black text-brand-400">50%</div>
          <div class="text-xs font-bold text-white uppercase tracking-wider">Direct Maintainer Share</div>
          <div class="text-[11px] text-gray-400">Credited on every verified click</div>
        </div>
        <div class="glass-card rounded-2xl p-5 text-center space-y-1 border-accent-500/20">
          <div class="text-3xl sm:text-4xl font-black text-accent-400">7</div>
          <div class="text-xs font-bold text-white uppercase tracking-wider">Dynamic Layout Styles</div>
          <div class="text-[11px] text-gray-400">From hero banners to Shields.io pills</div>
        </div>
        <div class="glass-card rounded-2xl p-5 text-center space-y-1 border-purple-500/20">
          <div class="text-3xl sm:text-4xl font-black text-purple-400">9</div>
          <div class="text-xs font-bold text-white uppercase tracking-wider">Developer Color Themes</div>
          <div class="text-[11px] text-gray-400">Dracula, Nord, Cyberpunk &amp; more</div>
        </div>
        <div class="glass-card rounded-2xl p-5 text-center space-y-1 border-pink-500/20">
          <div class="text-3xl sm:text-4xl font-black text-pink-400">100%</div>
          <div class="text-xs font-bold text-white uppercase tracking-wider">Anti-Fraud Deduplication</div>
          <div class="text-[11px] text-gray-400">Irreversible SHA-256 client audit hash</div>
        </div>
      </div>

      <!-- TWO-SIDED MARKETPLACE EXPLANATION -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 pt-4">
        <!-- For Maintainers -->
        <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5 border-brand-500/30">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
              <i data-lucide="code-2" class="w-5 h-5"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">For Independent Maintainers</h3>
              <p class="text-xs text-brand-300">Earn monthly compensation without compromising your code</p>
            </div>
          </div>
          <div class="space-y-3.5 text-xs text-gray-300">
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">1</span>
              <div>
                <strong class="text-white">One-Click GitHub OAuth Verification:</strong>
                <p class="text-gray-400 mt-0.5">Authenticate with GitHub. We automatically discover and enroll all public repositories you own.</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">2</span>
              <div>
                <strong class="text-white">Unlock the Interactive Maintainer Studio:</strong>
                <p class="text-gray-400 mt-0.5">Pick from 7 layout styles (Glass Banner, Linear Dark, Spotlight, Backer Pill, Goal Bar), choose your theme, and paste one line of Markdown into your README.</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">3</span>
              <div>
                <strong class="text-white">Dependable 50/50 Monthly Payouts:</strong>
                <p class="text-gray-400 mt-0.5">Every verified click splits 50% directly to your balance. Payouts disburse automatically via PayPal MassPay or crypto.</p>
              </div>
            </div>
          </div>
          <div class="pt-2">
            <button onclick="loginWithGitHubForDashboard()" class="w-full py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-bold text-xs transition flex items-center justify-center space-x-2">
              <i data-lucide="award" class="w-4 h-4"></i>
              <span>Open Maintainer Hub &amp; Unlock Studio</span>
            </button>
          </div>
        </div>

        <!-- For Sponsors -->
        <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5 border-accent-500/30">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-accent-500/10 border border-accent-500/20 flex items-center justify-center text-accent-400">
              <i data-lucide="megaphone" class="w-5 h-5"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">For Tech Sponsors &amp; Advertisers</h3>
              <p class="text-xs text-accent-300">Reach thousands of active engineers where they build software</p>
            </div>
          </div>
          <div class="space-y-3.5 text-xs text-gray-300">
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-accent-500/20 text-accent-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">1</span>
              <div>
                <strong class="text-white">Laser-Target by Language Ecosystem:</strong>
                <p class="text-gray-400 mt-0.5">Target developers coding in Python, Rust, TypeScript, Go, or sponsor specific flagship projects exclusively.</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-accent-500/20 text-accent-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">2</span>
              <div>
                <strong class="text-white">Impervious to Ad-Blockers:</strong>
                <p class="text-gray-400 mt-0.5">Badges compile natively as W3C SVG images directly inside GitHub READMEs, delivering 100% impression visibility.</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <span class="w-5 h-5 rounded-full bg-accent-500/20 text-accent-400 flex items-center justify-center font-bold text-[11px] flex-shrink-0 mt-0.5">3</span>
              <div>
                <strong class="text-white">Verifiable Deduplicated Analytics:</strong>
                <p class="text-gray-400 mt-0.5">Real-time CTR tracking, remaining impression budget, and instant top-ups via PayPal Checkout or USDC/Crypto.</p>
              </div>
            </div>
          </div>
          <div class="pt-2">
            <button onclick="switchTab('sponsors')" class="w-full py-2.5 rounded-lg bg-accent-600 hover:bg-accent-500 text-white font-bold text-xs transition flex items-center justify-center space-x-2">
              <i data-lucide="external-link" class="w-4 h-4"></i>
              <span>Enter Sponsor Dashboard &amp; Campaigns</span>
            </button>
          </div>
        </div>
      </div>

      <!-- ===================================================================== -->
      <!-- COMPREHENSIVE BADGE STYLES & OPTIONS SHOWCASE (GALLERY)               -->
      <!-- ===================================================================== -->
      <div id="badge-showcase-section" class="pt-8 space-y-8 border-t border-gray-800">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-[11px] font-semibold uppercase tracking-wider mb-2">
              <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
              <span>Visual Customization Suite</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Badge Styles &amp; Options Gallery
            </h2>
            <p class="text-gray-400 text-sm mt-1 max-w-2xl">
              Compare all 7 layout designs, 9 developer color themes, and query options. Lock in the perfect look for your repository README.
            </p>
          </div>
          <div class="flex items-center space-x-2 text-xs">
            <span class="text-gray-500 font-medium">Jump to:</span>
            <a href="#showcase-styles" class="px-2.5 py-1 rounded bg-gray-800 text-gray-300 hover:text-white border border-gray-700 transition">Styles (7)</a>
            <a href="#showcase-themes" class="px-2.5 py-1 rounded bg-gray-800 text-gray-300 hover:text-white border border-gray-700 transition">Themes (9)</a>
            <a href="#showcase-parameters" class="px-2.5 py-1 rounded bg-gray-800 text-gray-300 hover:text-white border border-gray-700 transition">URL Parameters</a>
          </div>
        </div>

        <!-- 7 STYLES COMPARISON GRID -->
        <div id="showcase-styles" class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          <!-- Style 1: Glass Banner -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-brand-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
                  <i data-lucide="layout" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">1. Glass Banner <span class="text-xs text-brand-400 font-normal">(Default)</span></h3>
                  <p class="text-[11px] text-gray-400">Hero banner for top of README or documentation</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">500 &times; 110 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center">
              <img src="/badge/tiangolo/fastapi.svg?style=banner&theme=dark" alt="Glass Banner Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=banner</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('banner', 'dark')" class="px-2.5 py-1 rounded text-xs font-semibold bg-brand-500/15 hover:bg-brand-500/25 text-brand-300 border border-brand-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-brand-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('banner', 'dark')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 2: Neo-Brutalist Linear Dark -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-purple-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                  <i data-lucide="terminal" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">2. Neo-Brutalist / Linear Dark</h3>
                  <p class="text-[11px] text-gray-400">Terminal typography, radial glow &amp; developer partner badge</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">500 &times; 110 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center">
              <img src="/badge/tiangolo/fastapi.svg?style=linear&theme=linear" alt="Linear Dark Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=linear&amp;theme=linear</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('linear', 'linear')" class="px-2.5 py-1 rounded text-xs font-semibold bg-purple-500/15 hover:bg-purple-500/25 text-purple-300 border border-purple-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-purple-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('linear', 'linear')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 3: Dual-Pill Radial Spotlight -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-pink-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-pink-500/10 border border-pink-500/20 flex items-center justify-center text-pink-400">
                  <i data-lucide="sparkles" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">3. Dual-Pill Radial Spotlight</h3>
                  <p class="text-[11px] text-gray-400">Two inset cards showcasing author stats &amp; featured sponsor</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">500 &times; 110 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center">
              <img src="/badge/tiangolo/fastapi.svg?style=spotlight&theme=synthwave" alt="Spotlight Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=spotlight&amp;theme=synthwave</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('spotlight', 'synthwave')" class="px-2.5 py-1 rounded text-xs font-semibold bg-pink-500/15 hover:bg-pink-500/25 text-pink-300 border border-pink-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-pink-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('spotlight', 'synthwave')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 4: Compact Micro-Card -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-cyan-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                  <i data-lucide="minimize-2" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">4. Compact Micro-Card</h3>
                  <p class="text-[11px] text-gray-400">Streamlined single-line layout with inline sponsor chip</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">500 &times; 110 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center">
              <img src="/badge/tiangolo/fastapi.svg?style=compact&theme=nord" alt="Compact Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=compact&amp;theme=nord</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('compact', 'nord')" class="px-2.5 py-1 rounded text-xs font-semibold bg-cyan-500/15 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-cyan-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('compact', 'nord')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 5: Dedicated Supporter / Backer Pill -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-rose-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
                  <i data-lucide="heart" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">5. Dedicated Supporter / Backer Badge</h3>
                  <p class="text-[11px] text-gray-400">Displays active backer or invites visitors to become project backer</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">320 &times; 28 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center py-5">
              <img src="/badge/tiangolo/fastapi.svg?style=backer&theme=dracula" alt="Backer Pill Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=backer&amp;theme=dracula</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('backer', 'dracula')" class="px-2.5 py-1 rounded text-xs font-semibold bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-rose-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('backer', 'dracula')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 6: Monthly Funding Goal Badge -->
          <div class="glass-panel rounded-2xl p-5 border border-gray-800 hover:border-emerald-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <i data-lucide="target" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">6. Monthly Funding Goal Progress Bar</h3>
                  <p class="text-[11px] text-gray-400">Crowdfunding sustainability tracker with animated progress fill</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">300 &times; 28 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center py-5">
              <img src="/badge/tiangolo/fastapi.svg?style=goal&theme=emerald" alt="Funding Goal Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=goal&amp;theme=emerald</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('goal', 'emerald')" class="px-2.5 py-1 rounded text-xs font-semibold bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-emerald-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('goal', 'emerald')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Style 7: Single-Line Shield Marquee Pill (Spans Full Width on LG) -->
          <div class="lg:col-span-2 glass-panel rounded-2xl p-5 border border-gray-800 hover:border-cyan-500/40 transition space-y-3.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span class="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                  <i data-lucide="shield" class="w-4 h-4"></i>
                </span>
                <div>
                  <h3 class="text-sm font-bold text-white">7. Shields.io Single-Line Marquee Pill</h3>
                  <p class="text-[11px] text-gray-400">Fits seamlessly into horizontal badge clusters; features smooth scrolling sponsor ticker</p>
                </div>
              </div>
              <span class="px-2 py-0.5 rounded text-[11px] font-mono bg-gray-800 text-gray-300 border border-gray-700">520 &times; 28 px</span>
            </div>
            <div class="p-3 bg-gray-950 rounded-xl border border-gray-800/80 overflow-x-auto flex justify-center py-5">
              <img src="/badge/tiangolo/fastapi.svg?style=shield&theme=cyberpunk" alt="Shield Pill Preview" class="max-w-full h-auto rounded shadow-lg">
            </div>
            <div class="flex items-center justify-between pt-1">
              <span class="text-[11px] font-mono text-gray-500">?style=shield&amp;theme=cyberpunk</span>
              <div class="flex items-center space-x-2">
                <button onclick="openMaintainerStudio('shield', 'cyberpunk')" class="px-2.5 py-1 rounded text-xs font-semibold bg-cyan-500/15 hover:bg-cyan-500/25 text-cyan-300 border border-cyan-500/30 transition flex items-center space-x-1">
                  <i data-lucide="lock" class="w-3 h-3 text-cyan-400"></i>
                  <span>Customize in Studio</span>
                </button>
                <button onclick="copySnippetForStyle('shield', 'cyberpunk')" class="px-2.5 py-1 rounded text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center space-x-1">
                  <i data-lucide="copy" class="w-3 h-3"></i>
                  <span>Copy Markdown</span>
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- 9 THEMES INTERACTIVE SWATCH PALETTE -->
        <div id="showcase-themes" class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-800 pb-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                <i data-lucide="palette" class="w-5 h-5 text-brand-400"></i>
                <span>Supported Color Palettes (9 Themes)</span>
              </h3>
              <p class="text-xs text-gray-400 mt-0.5">Click any palette swatch to apply it directly to your badge preview.</p>
            </div>
            <span class="text-xs text-gray-500 font-mono">?theme=&lt;name&gt;</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-3">
            <button onclick="openMaintainerStudio(currentBadgeStyle, 'dark')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-brand-500 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#111620] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#58a6ff]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#2ea043]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-brand-300">Dark</div>
              <div class="text-[10px] text-gray-500">Classic Obsidian</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'cyberpunk')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-pink-500 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#0d0221] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#00f0ff]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#f43f5e]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-pink-300">Cyberpunk</div>
              <div class="text-[10px] text-gray-500">Neon &amp; Cyan</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'emerald')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-emerald-500 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#062016] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#10b981]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#34d399]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-emerald-300">Emerald</div>
              <div class="text-[10px] text-gray-500">Forest Jade</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'light')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-blue-400 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#ffffff] border border-gray-400"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#0969da]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#2da44e]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-blue-300">Light</div>
              <div class="text-[10px] text-gray-500">Clean White</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'linear')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-purple-400 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#08090d] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#a78bfa]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#7c3aed]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-purple-300">Linear</div>
              <div class="text-[10px] text-gray-500">Vercel Violet</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'dracula')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-purple-300 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#282a36] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#bd93f9]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#50fa7b]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-purple-200">Dracula</div>
              <div class="text-[10px] text-gray-500">Goth Neon</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'nord')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-cyan-400 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#242933] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#88c0d0]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#81a1c1]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-cyan-300">Nord</div>
              <div class="text-[10px] text-gray-500">Arctic Frost</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'monokai')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-yellow-400 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#1e1f1c] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#66d9ef]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#a6e22e]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-yellow-300">Monokai</div>
              <div class="text-[10px] text-gray-500">Charcoal Gold</div>
            </button>

            <button onclick="openMaintainerStudio(currentBadgeStyle, 'synthwave')" class="p-3 rounded-xl bg-gray-950 border border-gray-800 hover:border-pink-400 text-left transition space-y-2 group">
              <div class="flex space-x-1">
                <span class="w-3.5 h-3.5 rounded-full bg-[#1a102f] border border-gray-700"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#01cdfe]"></span>
                <span class="w-3.5 h-3.5 rounded-full bg-[#ff71ce]"></span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-pink-300">Synthwave</div>
              <div class="text-[10px] text-gray-500">80s Sunset</div>
            </button>
          </div>
        </div>

        <!-- URL PARAMETERS & CUSTOMIZATION CHEATSHEET -->
        <div id="showcase-parameters" class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5">
          <div class="flex items-center justify-between border-b border-gray-800 pb-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                <i data-lucide="sliders-horizontal" class="w-5 h-5 text-accent-400"></i>
                <span>URL Parameters &amp; Usage Cheatsheet</span>
              </h3>
              <p class="text-xs text-gray-400 mt-0.5">Customize any badge URL directly in your README markdown or HTML.</p>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-gray-900/80 text-gray-400 uppercase tracking-wider font-semibold border-b border-gray-800">
                <tr>
                  <th class="px-4 py-3">Parameter</th>
                  <th class="px-4 py-3">Options</th>
                  <th class="px-4 py-3">Default</th>
                  <th class="px-4 py-3">What It Does</th>
                  <th class="px-4 py-3">Example Usage</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800 text-gray-300">
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-brand-300">style</td>
                  <td class="px-4 py-3 font-mono text-gray-400">banner, linear, spotlight, compact, backer, goal, shield</td>
                  <td class="px-4 py-3 font-mono text-gray-400">banner</td>
                  <td class="px-4 py-3">Selects one of the 7 visual layouts.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?style=linear</td>
                </tr>
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-accent-300">theme</td>
                  <td class="px-4 py-3 font-mono text-gray-400">dark, cyberpunk, emerald, light, linear, dracula, nord, monokai, synthwave</td>
                  <td class="px-4 py-3 font-mono text-gray-400">dark</td>
                  <td class="px-4 py-3">Switches color palette and gradient accents.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?theme=dracula</td>
                </tr>
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-pink-300">marquee</td>
                  <td class="px-4 py-3 font-mono text-gray-400">true, false</td>
                  <td class="px-4 py-3 font-mono text-gray-400">false (true on shield)</td>
                  <td class="px-4 py-3">Enables smooth right-to-left scrolling ticker on sponsor headline.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?marquee=true</td>
                </tr>
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-yellow-300">sponsor_pos</td>
                  <td class="px-4 py-3 font-mono text-gray-400">right, left</td>
                  <td class="px-4 py-3 font-mono text-gray-400">right</td>
                  <td class="px-4 py-3">Flips card layout: sponsor on left, repo stats on right.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?sponsor_pos=left</td>
                </tr>
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-purple-300">hide_stars</td>
                  <td class="px-4 py-3 font-mono text-gray-400">true, false</td>
                  <td class="px-4 py-3 font-mono text-gray-400">false</td>
                  <td class="px-4 py-3">Suppresses live star counter for cleaner look.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?hide_stars=true</td>
                </tr>
                <tr>
                  <td class="px-4 py-3 font-mono font-bold text-emerald-300">hide_ci</td>
                  <td class="px-4 py-3 font-mono text-gray-400">true, false</td>
                  <td class="px-4 py-3 font-mono text-gray-400">false</td>
                  <td class="px-4 py-3">Suppresses CI/CD build passing pill.</td>
                  <td class="px-4 py-3 font-mono text-gray-400">?hide_ci=true</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ETHICAL ADVERTISING & ZERO-MOCK MANIFESTO -->
      <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-4 border-gray-800">
        <div class="flex items-center space-x-3 text-white font-bold text-base">
          <i data-lucide="shield-alert" class="w-5 h-5 text-brand-400"></i>
          <span>Our Integrity Guarantee: Authentic Data Only</span>
        </div>
        <p class="text-xs text-gray-400 leading-relaxed">
          ReadmePay adheres to strict data integrity standards. We never inject synthetic people, mock dollar balances, or fake fiduciaries into production responses. If county records or GitHub repos are unindexed, our endpoints fail transparently with 404 or honest status messages. Every metric in your dashboard reflects real, verifiable I/O operations.
        </p>
      </div>

      <!-- BOTTOM CONVERSION CTA BANNER -->
      <div class="glass-panel rounded-2xl p-8 sm:p-10 text-center space-y-5 glow-emerald border-brand-500/30">
        <h2 class="text-3xl font-black text-white">Ready to Empower Your Open-Source Work?</h2>
        <p class="text-gray-300 text-sm max-w-xl mx-auto">
          Join hundreds of independent maintainers generating sustainable monthly income from their public repositories.
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <button onclick="loginWithGitHubForDashboard()" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-bold text-sm shadow-xl transition flex items-center justify-center space-x-2">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            <span>Sign in with GitHub to Claim Repos</span>
          </button>
          <button onclick="switchTab('sponsors')" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-gray-900 hover:bg-gray-800 text-accent-300 border border-accent-500/30 font-bold text-sm transition flex items-center justify-center space-x-2">
            <i data-lucide="megaphone" class="w-4 h-4 text-accent-400"></i>
            <span>Sponsor Open-Source Developers</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- TAB 2: REPO OWNER (MAINTAINER) DASHBOARD (LOCKED STUDIO INSIDE)           -->
    <!-- ========================================================================= -->
    <section id="tab-revenue" class="tab-content hidden space-y-8">
      <!-- 1. AUTHENTICATION GATE (Shown when maintainer is not logged in) -->
      <div id="maintainer-auth-gate" class="glass-panel rounded-2xl p-8 sm:p-12 text-center max-w-2xl mx-auto space-y-6 glow-emerald">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
          <i data-lucide="lock" class="w-8 h-8"></i>
        </div>
        <div class="space-y-2">
          <div class="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-[11px] font-semibold uppercase tracking-wider mb-1">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
            <span>Maintainer Security &amp; Studio Gate</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Maintainer Economic Hub &amp; Studio</h2>
          <p class="text-gray-400 text-sm max-w-md mx-auto leading-relaxed">
            To generate authorized README badges, protect revenue ownership, and configure monthly payouts, please authenticate with your GitHub account.
          </p>
        </div>

        <div class="p-4 bg-gray-950/70 border border-gray-800 rounded-xl text-left space-y-2 text-xs text-gray-300">
          <div class="flex items-center space-x-2 text-brand-300 font-semibold">
            <i data-lucide="shield-check" class="w-4 h-4 text-brand-400"></i>
            <span>Verified Ownership Guarantee</span>
          </div>
          <p class="text-gray-400 leading-relaxed text-[11px]">
            We use read-only GitHub OAuth verification to confirm you are the repository owner or collaborator. Only verified maintainers can view financials, unlock the Badge Studio, and register payout destinations.
          </p>
        </div>

        <div class="pt-2">
          <button onclick="loginWithGitHubForDashboard()" class="w-full sm:w-auto px-8 py-3.5 bg-[#24292f] hover:bg-[#1b1f23] border border-gray-600 text-white font-bold rounded-xl text-sm shadow-xl hover:shadow-brand-500/10 transition flex items-center justify-center space-x-3 mx-auto">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            <span>Sign in with GitHub to Access Dashboard &amp; Studio</span>
          </button>
        </div>
      </div>

      <!-- 2. MAINTAINER AUTHENTICATED DASHBOARD (Hidden until signed in) -->
      <div id="maintainer-authenticated-view" class="hidden space-y-8">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-5">
          <div>
            <div class="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-[11px] font-semibold uppercase tracking-wider mb-1">
              <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
              <span>Verified Maintainer: <span id="auth-maintainer-name">@username</span></span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Maintainer Economic Dashboard</h2>
            <p class="text-gray-400 text-xs sm:text-sm mt-0.5">Economic empowerment infrastructure: track portfolio revenue, impression yield, active sponsors, and automated 50/50 monthly distributions.</p>
          </div>

          <div class="flex items-center space-x-2">
            <button onclick="claimAllPublicRepos()" id="btn-claim-all-public" class="px-3 py-2 rounded-lg bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white text-xs font-bold shadow-md shadow-brand-500/20 transition flex items-center space-x-1.5">
              <i data-lucide="zap" class="w-3.5 h-3.5" id="icon-claim-all"></i>
              <span>Enroll All Public Repos</span>
            </button>
            <select id="select-claimed-repos" onchange="onSelectClaimedRepo(this.value)" class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500">
              <!-- Populated dynamically via JS -->
            </select>
            <a href="/api/auth/github/logout" class="px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white border border-gray-700 text-xs font-semibold transition flex items-center space-x-1">
              <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
              <span>Sign Out</span>
            </a>
          </div>
        </div>

        <!-- KPI Summary Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card rounded-xl p-4 space-y-1 border-brand-500/30">
            <div class="text-xs text-brand-400 font-semibold flex items-center justify-between">
              <span>Maintainer Share (50%)</span>
              <i data-lucide="wallet" class="w-4 h-4"></i>
            </div>
            <div id="kpi-maintainer" class="text-2xl font-black text-brand-300">$0.00</div>
            <div class="text-[10px] text-brand-500/80">Available for Payout</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Gross Ad Spend</span>
              <i data-lucide="dollar-sign" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div id="kpi-gross" class="text-2xl font-black text-white">$0.00</div>
            <div class="text-[10px] text-gray-500">Total Sponsor Budget Spent</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Verified Clicks</span>
              <i data-lucide="mouse-pointer-click" class="w-4 h-4 text-accent-400"></i>
            </div>
            <div id="kpi-clicks" class="text-2xl font-black text-white">0 Clicks</div>
            <div class="text-[10px] text-gray-500">SHA-256 Deduplicated</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Claimed Repos</span>
              <i data-lucide="git-pull-request" class="w-4 h-4 text-pink-400"></i>
            </div>
            <div id="maintainer-repo-count" class="text-2xl font-black text-pink-300">0 of 0</div>
            <div class="text-[10px] text-gray-500">Monetization Active</div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- THE INTERACTIVE BADGE STUDIO & SNIPPET GENERATOR (LOCKED HERE)      -->
        <!-- =================================================================== -->
        <div id="studio-sandbox" class="glass-panel rounded-2xl p-6 sm:p-8 glow-emerald space-y-6">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-800 pb-5">
            <div>
              <h2 class="text-xl font-bold text-white flex items-center space-x-2">
                <i data-lucide="sliders" class="w-5 h-5 text-brand-400"></i>
                <span>Interactive Badge Studio &amp; Snippet Generator</span>
              </h2>
              <p class="text-sm text-gray-400 mt-0.5">Customize your badge layout, test color themes, and generate copy-pasteable README Markdown.</p>
            </div>

            <!-- Repository Quick Selector -->
            <div class="flex items-center space-x-2">
              <span class="text-xs text-gray-400 font-semibold">Active Repository:</span>
              <select id="studio-repo-selector" onchange="onStudioRepoSelect(this.value)" class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-brand-500">
                <!-- Populated dynamically via JS -->
              </select>
            </div>
          </div>

          <!-- Input Bar -->
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
            <div class="sm:col-span-4">
              <label class="block text-xs font-semibold text-gray-400 mb-1">GitHub Owner / Org</label>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">@</span>
                <input type="text" id="input-owner" value="tiangolo" placeholder="e.g. tiangolo" class="w-full bg-gray-900/90 border border-gray-700 rounded-lg pl-8 pr-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
              </div>
            </div>
            <div class="sm:col-span-5">
              <label class="block text-xs font-semibold text-gray-400 mb-1">Repository Name</label>
              <input type="text" id="input-repo" value="fastapi" placeholder="e.g. fastapi" class="w-full bg-gray-900/90 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
            </div>
            <div class="sm:col-span-3 flex items-end">
              <button onclick="renderStudioBadge()" id="btn-generate" class="w-full bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white font-semibold py-2 px-4 rounded-lg text-sm shadow-md shadow-brand-600/30 transition flex items-center justify-center space-x-2">
                <i data-lucide="refresh-cw" class="w-4 h-4" id="icon-refresh"></i>
                <span>Render Badge</span>
              </button>
            </div>
          </div>

          <!-- Live Preview Stage -->
          <div class="bg-gray-950 rounded-xl border border-gray-800 p-6 flex flex-col items-center justify-center space-y-4 relative overflow-hidden">
            <div class="flex items-center justify-between w-full">
              <div class="text-xs uppercase tracking-widest text-gray-500 font-semibold flex items-center space-x-2">
                <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                <span>Live Compiled SVG Output</span>
              </div>
              <!-- Badge Format Selector (7 styles) -->
              <div class="flex items-center space-x-1 bg-gray-900 border border-gray-800 p-1 rounded-lg flex-wrap">
                <button onclick="setStudioStyle('banner')" id="btn-style-banner" class="px-2.5 py-1 text-xs rounded font-medium text-brand-300 bg-brand-500/15 border border-brand-500/30 transition flex items-center space-x-1">
                  <i data-lucide="layout" class="w-3 h-3"></i>
                  <span>Glass Banner</span>
                </button>
                <button onclick="setStudioStyle('linear')" id="btn-style-linear" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="terminal" class="w-3 h-3"></i>
                  <span>Linear Dark</span>
                </button>
                <button onclick="setStudioStyle('spotlight')" id="btn-style-spotlight" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="sparkles" class="w-3 h-3"></i>
                  <span>Spotlight</span>
                </button>
                <button onclick="setStudioStyle('compact')" id="btn-style-compact" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="minimize-2" class="w-3 h-3"></i>
                  <span>Compact</span>
                </button>
                <button onclick="setStudioStyle('backer')" id="btn-style-backer" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="heart" class="w-3 h-3 text-pink-400"></i>
                  <span>Backer Pill</span>
                </button>
                <button onclick="setStudioStyle('goal')" id="btn-style-goal" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="target" class="w-3 h-3 text-emerald-400"></i>
                  <span>Goal Bar</span>
                </button>
                <button onclick="setStudioStyle('shield')" id="btn-style-shield" class="px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1">
                  <i data-lucide="shield" class="w-3 h-3"></i>
                  <span>Shield Pill</span>
                </button>
              </div>
            </div>

            <!-- Studio Customization Controls Bar -->
            <div class="w-full bg-gray-900/60 border border-gray-800/80 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 text-xs">
              <!-- Theme Selection (9 themes) -->
              <div class="flex items-center space-x-2 flex-wrap gap-y-1.5">
                <span class="text-gray-400 font-semibold flex items-center space-x-1">
                  <i data-lucide="palette" class="w-3.5 h-3.5 text-brand-400"></i>
                  <span>Theme:</span>
                </span>
                <div class="flex items-center space-x-1 bg-gray-950 p-1 rounded-lg border border-gray-800 flex-wrap">
                  <button type="button" onclick="setStudioTheme('dark')" id="theme-btn-dark" class="px-2 py-0.5 rounded text-[11px] font-medium bg-brand-500/20 text-brand-300 border border-brand-500/30">Dark</button>
                  <button type="button" onclick="setStudioTheme('cyberpunk')" id="theme-btn-cyberpunk" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-pink-300">Cyberpunk</button>
                  <button type="button" onclick="setStudioTheme('emerald')" id="theme-btn-emerald" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-emerald-300">Emerald</button>
                  <button type="button" onclick="setStudioTheme('light')" id="theme-btn-light" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-gray-200">Light</button>
                  <button type="button" onclick="setStudioTheme('linear')" id="theme-btn-linear" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-purple-300">Linear</button>
                  <button type="button" onclick="setStudioTheme('dracula')" id="theme-btn-dracula" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-purple-200">Dracula</button>
                  <button type="button" onclick="setStudioTheme('nord')" id="theme-btn-nord" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-cyan-300">Nord</button>
                  <button type="button" onclick="setStudioTheme('monokai')" id="theme-btn-monokai" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-yellow-300">Monokai</button>
                  <button type="button" onclick="setStudioTheme('synthwave')" id="theme-btn-synthwave" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-pink-400">Synthwave</button>
                </div>
              </div>

              <!-- Sponsor Positioning -->
              <div id="wrapper-sponsor-pos" class="flex items-center space-x-2">
                <span class="text-gray-400 font-semibold flex items-center space-x-1">
                  <i data-lucide="arrow-left-right" class="w-3.5 h-3.5 text-accent-400"></i>
                  <span>Sponsor Spot:</span>
                </span>
                <div class="flex items-center space-x-1 bg-gray-950 p-1 rounded-lg border border-gray-800">
                  <button type="button" onclick="setStudioSponsorPos('right')" id="pos-btn-right" class="px-2 py-0.5 rounded text-[11px] font-medium bg-brand-500/20 text-brand-300 border border-brand-500/30">Right (Default)</button>
                  <button type="button" onclick="setStudioSponsorPos('left')" id="pos-btn-left" class="px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-white">Left (Featured)</button>
                </div>
              </div>

              <!-- Marquee Toggle -->
              <div id="wrapper-marquee-toggle" class="flex items-center space-x-2">
                <label class="flex items-center space-x-1.5 cursor-pointer text-gray-300">
                  <input type="checkbox" id="check-marquee" onchange="toggleStudioMarquee()" class="rounded border-gray-700 text-brand-500 focus:ring-brand-500">
                  <span class="font-semibold text-brand-300 flex items-center space-x-1">
                    <i data-lucide="play-circle" class="w-3.5 h-3.5"></i>
                    <span>Sponsor Marquee Ticker</span>
                  </span>
                </label>
              </div>

              <!-- Stat Toggles -->
              <div class="flex items-center space-x-3">
                <label class="flex items-center space-x-1.5 cursor-pointer text-gray-400 hover:text-gray-200">
                  <input type="checkbox" id="check-hide-stars" onchange="toggleStudioStats()" class="rounded border-gray-700 text-brand-500 focus:ring-brand-500">
                  <span>Hide Stars</span>
                </label>
                <label class="flex items-center space-x-1.5 cursor-pointer text-gray-400 hover:text-gray-200">
                  <input type="checkbox" id="check-hide-ci" onchange="toggleStudioStats()" class="rounded border-gray-700 text-brand-500 focus:ring-brand-500">
                  <span>Hide CI</span>
                </label>
              </div>
            </div>

            <!-- The Live Badge Image -->
            <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800 shadow-inner max-w-full overflow-x-auto flex justify-center">
              <img id="badge-preview-img" src="/badge/tiangolo/fastapi.svg" alt="Dynamic Sponsorship Badge" class="max-w-full h-auto rounded transition duration-200" onerror="handlePreviewError()">
            </div>

            <div id="preview-meta" class="flex flex-wrap items-center justify-center gap-4 text-xs text-gray-400">
              <span id="preview-stars" class="flex items-center space-x-1"><i data-lucide="star" class="w-3.5 h-3.5 text-yellow-400"></i><span>Loading stats...</span></span>
              <span id="preview-lang" class="flex items-center space-x-1"><i data-lucide="code" class="w-3.5 h-3.5 text-cyan-400"></i><span>Language: ...</span></span>
              <span id="preview-sponsor" class="flex items-center space-x-1"><i data-lucide="heart" class="w-3.5 h-3.5 text-pink-400"></i><span>Matched: ...</span></span>
            </div>

            <div class="flex items-center space-x-3 pt-2">
              <a id="btn-test-click" href="#" target="_blank" class="px-3.5 py-1.5 rounded-lg bg-brand-500/15 hover:bg-brand-500/25 border border-brand-500/30 text-brand-300 text-xs font-semibold transition flex items-center space-x-1.5">
                <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                <span>Test Click &amp; 302 Redirect</span>
              </a>
            </div>
          </div>

          <!-- Copy-Paste Snippet Box with Tabs -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="text-xs font-bold uppercase tracking-wider text-gray-400">Embed Snippets:</span>
                <button onclick="setSnippetTab('markdown')" id="btn-snip-markdown" class="snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-brand-300 bg-brand-500/10 border border-brand-500/30">Markdown</button>
                <button onclick="setSnippetTab('shieldsio')" id="btn-snip-shieldsio" class="snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-emerald-400 hover:text-emerald-300 bg-emerald-500/10 border border-emerald-500/30">Shields.io</button>
                <button onclick="setSnippetTab('html')" id="btn-snip-html" class="snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-gray-400 hover:text-gray-200">HTML</button>
                <button onclick="setSnippetTab('rst')" id="btn-snip-rst" class="snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-gray-400 hover:text-gray-200">RST</button>
                <button onclick="setSnippetTab('urls')" id="btn-snip-urls" class="snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-gray-400 hover:text-gray-200">Direct URLs</button>
              </div>
              <button onclick="copyCurrentSnippet()" class="px-3 py-1 rounded bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition flex items-center space-x-1.5 shadow">
                <i data-lucide="copy" class="w-3.5 h-3.5" id="copy-icon"></i>
                <span id="copy-btn-text">Copy Snippet</span>
              </button>
            </div>

            <div class="relative">
              <textarea id="snippet-code-box" readonly rows="3" class="w-full bg-gray-950 border border-gray-800 rounded-xl p-3.5 text-xs text-brand-200 font-mono focus:outline-none focus:border-brand-500 resize-none"></textarea>
            </div>
          </div>
        </div>

        <!-- Portfolio Table & Payout Destination -->
        <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                <i data-lucide="wallet" class="w-5 h-5 text-brand-400"></i>
                <span>Automated Payout Destination</span>
              </h3>
              <p class="text-xs text-gray-400 mt-0.5">50% revenue share is automatically disbursed monthly to your designated address.</p>
            </div>
            <div class="flex items-center space-x-2">
              <input type="text" id="input-global-payout" placeholder="PayPal email or crypto address" class="bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-brand-500 w-64">
              <button onclick="saveGlobalPayout()" class="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition flex items-center space-x-1">
                <i data-lucide="save" class="w-3.5 h-3.5"></i>
                <span>Save Payout</span>
              </button>
            </div>
          </div>

          <!-- Claimed Repos Portfolio Table -->
          <div>
            <h4 class="text-sm font-bold text-white mb-3">Your Public Repositories &amp; Monetization Status</h4>
            <div class="overflow-x-auto rounded-xl border border-gray-800">
              <table class="w-full text-left text-xs">
                <thead class="bg-gray-900/80 text-gray-400 uppercase tracking-wider font-semibold border-b border-gray-800">
                  <tr>
                    <th class="px-4 py-3">Repository</th>
                    <th class="px-4 py-3">Stars</th>
                    <th class="px-4 py-3">Monetization</th>
                    <th class="px-4 py-3">Maintainer Earnings</th>
                    <th class="px-4 py-3">Verified Clicks</th>
                    <th class="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody id="maintainer-portfolio-table-body" class="divide-y divide-gray-800 text-gray-300">
                  <!-- Loaded via JS -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- TAB 3: SPONSOR / ADVERTISER HUB & CAMPAIGN DASHBOARD                     -->
    <!-- ========================================================================= -->
    <section id="tab-sponsors" class="tab-content hidden space-y-8">
      
      <!-- 1. SPONSOR LOGIN / ACCESS GATE (Shown when sponsor is not logged in) -->
      <div id="sponsor-login-gate" class="space-y-8">
        <!-- Visual Sponsor Hero -->
        <div class="text-center max-w-3xl mx-auto space-y-4 pt-4">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-accent-500/10 border border-accent-500/20 text-accent-400 text-xs font-semibold uppercase tracking-wider">
            <i data-lucide="megaphone" class="w-3.5 h-3.5"></i>
            <span>Advertiser Growth Center &amp; Campaign Hub</span>
          </div>
          <h2 class="text-3xl sm:text-5xl font-black text-white tracking-tight">
            Sponsor Open-Source Ecosystems
          </h2>
          <p class="text-gray-300 text-sm sm:text-base leading-relaxed max-w-2xl mx-auto">
            Reach 100,000+ active software engineers natively inside high-traffic GitHub README files. 0% ad-blocker loss. 50% revenue directly sustains open-source creators.
          </p>
        </div>

        <!-- 2-Column Sponsor Access Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          <!-- Card 1: Sponsor Login -->
          <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5 border-accent-500/30">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-xl bg-accent-500/10 border border-accent-500/20 flex items-center justify-center text-accent-400">
                <i data-lucide="log-in" class="w-5 h-5"></i>
              </div>
              <div>
                <h3 class="text-lg font-bold text-white">Sign In to Sponsor Dashboard</h3>
                <p class="text-xs text-gray-400">Access your active campaigns, budget &amp; click analytics</p>
              </div>
            </div>

            <form onsubmit="handleSponsorLoginForm(event)" class="space-y-4 text-xs">
              <div>
                <label class="block font-semibold text-gray-300 mb-1">Company or Brand Name <span class="text-rose-400">*</span></label>
                <input type="text" id="input-sponsor-name" required placeholder="e.g. Supabase, Neon, Datadog" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3.5 py-2.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-accent-500">
              </div>

              <!-- Quick Demo Login Pills -->
              <div class="space-y-1.5 pt-1">
                <span class="text-[11px] text-gray-500 font-medium">Quick Access (Existing Sponsors):</span>
                <div class="flex items-center space-x-1.5 flex-wrap gap-y-1">
                  <button type="button" onclick="quickSponsorLogin('Supabase')" class="px-2 py-0.5 rounded text-[11px] bg-gray-800 hover:bg-accent-900/40 text-gray-300 hover:text-accent-300 border border-gray-700 transition">Supabase</button>
                  <button type="button" onclick="quickSponsorLogin('Neon')" class="px-2 py-0.5 rounded text-[11px] bg-gray-800 hover:bg-accent-900/40 text-gray-300 hover:text-accent-300 border border-gray-700 transition">Neon</button>
                  <button type="button" onclick="quickSponsorLogin('Pinecone')" class="px-2 py-0.5 rounded text-[11px] bg-gray-800 hover:bg-accent-900/40 text-gray-300 hover:text-accent-300 border border-gray-700 transition">Pinecone</button>
                </div>
              </div>

              <button type="submit" id="btn-sponsor-login" class="w-full py-3 rounded-lg bg-accent-600 hover:bg-accent-500 text-white font-bold text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-accent-600/20">
                <i data-lucide="log-in" class="w-4 h-4"></i>
                <span>Sign In to Sponsor Dashboard</span>
              </button>
            </form>
          </div>

          <!-- Card 2: Launch Campaign -->
          <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-5 border-brand-500/30 flex flex-col justify-between">
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
                  <i data-lucide="plus-circle" class="w-5 h-5"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-white">New Sponsor? Launch in Minutes</h3>
                  <p class="text-xs text-gray-400">Fund via PayPal Checkout or USDC / Crypto</p>
                </div>
              </div>
              <p class="text-xs text-gray-300 leading-relaxed">
                Create a high-impact sponsorship campaign targeted by programming language (Python, Rust, TS, Go) or directly sponsor an exclusive open-source repository.
              </p>
              <div class="space-y-2 text-xs text-gray-400">
                <div class="flex items-center space-x-2"><i data-lucide="check" class="w-3.5 h-3.5 text-brand-400"></i><span>Minimum deposit from $5.00</span></div>
                <div class="flex items-center space-x-2"><i data-lucide="check" class="w-3.5 h-3.5 text-brand-400"></i><span>Instant PayPal Orders v2 &amp; Crypto Rails</span></div>
                <div class="flex items-center space-x-2"><i data-lucide="check" class="w-3.5 h-3.5 text-brand-400"></i><span>Verifiable, deduplicated developer clicks</span></div>
              </div>
            </div>
            <button onclick="openCreateCampaignModal()" class="w-full py-3 rounded-lg bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white font-bold text-xs transition flex items-center justify-center space-x-2 shadow-lg shadow-brand-500/20">
              <i data-lucide="sparkles" class="w-4 h-4"></i>
              <span>Create &amp; Fund New Campaign</span>
            </button>
          </div>
        </div>

        <!-- Public Active Campaigns Catalog -->
        <div class="pt-6 space-y-4">
          <div class="flex items-center justify-between border-b border-gray-800 pb-3">
            <div>
              <h3 class="text-lg font-bold text-white">Live Platform Campaigns (Public Directory)</h3>
              <p class="text-xs text-gray-400">Explore authentic tech sponsorships currently running across open-source READMEs.</p>
            </div>
          </div>
          <div id="sponsors-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Dynamic Cards Loaded via JS -->
          </div>
        </div>
      </div>

      <!-- 2. SPONSOR AUTHENTICATED DASHBOARD (Shown when sponsor is signed in) -->
      <div id="sponsor-authenticated-view" class="hidden space-y-8">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-5">
          <div>
            <div class="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-full bg-accent-500/10 border border-accent-500/20 text-accent-400 text-[11px] font-semibold uppercase tracking-wider mb-1">
              <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
              <span>Active Sponsor: <span id="auth-sponsor-name" class="font-bold text-white">CompanyName</span></span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Sponsor Campaign Dashboard</h2>
            <p class="text-gray-400 text-xs sm:text-sm mt-0.5">Manage impression balances, inspect verified developer click metrics, and fund your campaigns.</p>
          </div>

          <div class="flex items-center space-x-2">
            <button onclick="openCreateCampaignModal()" class="px-3.5 py-2 rounded-lg bg-gradient-to-r from-brand-600 to-accent-500 hover:from-brand-500 hover:to-accent-400 text-white text-xs font-bold shadow-lg shadow-brand-500/20 transition flex items-center space-x-1.5">
              <i data-lucide="plus-circle" class="w-3.5 h-3.5"></i>
              <span>New Campaign</span>
            </button>
            <button onclick="logoutSponsor()" class="px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white border border-gray-700 text-xs font-semibold transition flex items-center space-x-1">
              <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
              <span>Sign Out</span>
            </button>
          </div>
        </div>

        <!-- Sponsor KPI Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Your Campaigns</span>
              <i data-lucide="activity" class="w-4 h-4 text-brand-400"></i>
            </div>
            <div id="sp-kpi-campaigns" class="text-2xl font-black text-white">0</div>
            <div class="text-[10px] text-gray-500">Live in GitHub READMEs</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Remaining Budget</span>
              <i data-lucide="wallet" class="w-4 h-4 text-accent-400"></i>
            </div>
            <div id="sp-kpi-budget" class="text-2xl font-black text-accent-300">$0.00</div>
            <div class="text-[10px] text-gray-500">Available Impression Balance</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Delivered Clicks</span>
              <i data-lucide="mouse-pointer-click" class="w-4 h-4 text-emerald-400"></i>
            </div>
            <div id="sp-kpi-clicks" class="text-2xl font-black text-brand-300">0 Clicks</div>
            <div id="sp-kpi-ctr" class="text-[10px] text-brand-400/80">Avg CTR: 0.0%</div>
          </div>

          <div class="glass-card rounded-xl p-4 space-y-1">
            <div class="text-xs text-gray-400 font-medium flex items-center justify-between">
              <span>Total Spent</span>
              <i data-lucide="tag" class="w-4 h-4 text-pink-400"></i>
            </div>
            <div id="sp-kpi-spent" class="text-2xl font-black text-pink-300">$0.00</div>
            <div class="text-[10px] text-gray-500">50% funded directly to authors</div>
          </div>
        </div>

        <!-- Sponsor Campaigns List -->
        <div class="glass-panel rounded-2xl p-6 sm:p-8 space-y-6">
          <div class="flex items-center justify-between border-b border-gray-800 pb-4">
            <h3 class="text-lg font-bold text-white flex items-center space-x-2">
              <i data-lucide="layers" class="w-5 h-5 text-accent-400"></i>
              <span>Your Active Sponsorship Campaigns</span>
            </h3>
            <button onclick="openCreateCampaignModal()" class="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition flex items-center space-x-1">
              <i data-lucide="plus" class="w-3.5 h-3.5"></i>
              <span>Add Campaign</span>
            </button>
          </div>

          <div id="sponsor-personal-campaigns-grid" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================================================= -->
    <!-- TAB 4: REPOSITORY INDEX & CATALOG                                         -->
    <!-- ========================================================================= -->
    <section id="tab-directory" class="tab-content hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-800 pb-5">
        <div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Repository Index</h2>
          <p class="text-gray-400 text-xs sm:text-sm mt-0.5">Top open-source repositories registered on the ReadmePay monetization network.</p>
        </div>
        <div class="w-full sm:w-72">
          <input type="text" id="dir-search-input" onkeyup="filterDirectoryTable()" placeholder="Filter by repository or language..." class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
        </div>
      </div>

      <div class="glass-panel rounded-2xl overflow-hidden border border-gray-800">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-gray-900/80 text-gray-400 uppercase tracking-wider font-semibold border-b border-gray-800">
              <tr>
                <th class="px-4 py-3">Repository</th>
                <th class="px-4 py-3">Stars</th>
                <th class="px-4 py-3">Primary Language</th>
                <th class="px-4 py-3">Claim Status</th>
                <th class="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody id="directory-table-body" class="divide-y divide-gray-800 text-gray-300">
              <!-- Loaded via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="mt-auto border-t border-gray-800/80 py-8 text-xs text-gray-500">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center space-x-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-brand-400"></i>
        <span>ReadmePay &mdash; Economic Empowerment Infrastructure for Independent Open-Source Developers.</span>
      </div>
      <div class="flex items-center space-x-4">
        <button onclick="openModal('privacy')" class="hover:text-gray-300 transition">Privacy Policy</button>
        <button onclick="openModal('terms')" class="hover:text-gray-300 transition">Terms of Service</button>
        <button onclick="openModal('security')" class="hover:text-gray-300 transition">Security Disclosure</button>
        <a href="/docs" target="_blank" class="hover:text-gray-300 transition">API Docs</a>
      </div>
    </div>
  </footer>

  <!-- CREATE & FUND AD CAMPAIGN MODAL -->
  <div id="modal-campaign" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-700 rounded-2xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl">
      <div class="p-6 border-b border-gray-800 flex items-center justify-between">
        <div class="flex items-center space-x-2 text-white font-bold text-base">
          <i data-lucide="megaphone" class="w-5 h-5 text-brand-400"></i>
          <span>Create &amp; Fund Sponsor Campaign</span>
        </div>
        <button onclick="closeCampaignModal()" class="text-gray-400 hover:text-white p-1 rounded-lg hover:bg-gray-800 transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <form id="form-create-campaign" onsubmit="submitNewCampaign(event)" class="p-6 overflow-y-auto space-y-4 text-xs">
        <div>
          <label class="block font-semibold text-gray-300 mb-1">Company / Product Name <span class="text-rose-400">*</span></label>
          <input type="text" id="ad-sponsor-name" required placeholder="e.g. Supabase, Datadog, Neon" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
        </div>

        <div>
          <label class="block font-semibold text-gray-300 mb-1">Headline Pitch <span class="text-rose-400">*</span></label>
          <input type="text" id="ad-headline" required placeholder="e.g. Serverless Postgres with instant branching" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
          <p class="text-[11px] text-gray-500 mt-1">Short, punchy pitch displayed inside the README badge ad card.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Target Language <span class="text-rose-400">*</span></label>
            <select id="ad-target-lang" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500">
              <option value="General">All Languages (General Fallback)</option>
              <option value="Python">Python</option>
              <option value="TypeScript">TypeScript / JavaScript</option>
              <option value="Rust">Rust</option>
              <option value="Go">Go (Golang)</option>
              <option value="Java">Java / Kotlin</option>
              <option value="C++">C / C++</option>
            </select>
          </div>
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Exclusive Target Repo (Optional)</label>
            <input type="text" id="ad-target-repo" placeholder="owner/repo (e.g. tiangolo/fastapi)" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Destination Click URL <span class="text-rose-400">*</span></label>
            <input type="url" id="ad-click-url" required placeholder="https://example.com/signup" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
          </div>
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Button Call to Action <span class="text-rose-400">*</span></label>
            <input type="text" id="ad-cta-text" required value="Learn More" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-brand-500">
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-gray-800">
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Impression Budget (USD) <span class="text-rose-400">*</span></label>
            <input type="number" id="ad-budget" required min="5" step="5" value="50" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500">
          </div>
          <div>
            <label class="block font-semibold text-gray-300 mb-1">Cost Per Click Bid (USD) <span class="text-rose-400">*</span></label>
            <input type="number" id="ad-cpc" required min="0.10" step="0.05" value="0.50" class="w-full bg-gray-950 border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500">
          </div>
        </div>

        <!-- Payment Rail Selector -->
        <div class="pt-3 border-t border-gray-800 space-y-2">
          <label class="block font-semibold text-gray-300">Payment Checkout Gateway <span class="text-rose-400">*</span></label>
          <div class="grid grid-cols-2 gap-3">
            <label class="flex items-center space-x-2 p-2.5 rounded-lg border border-gray-700 bg-gray-950/60 cursor-pointer hover:border-brand-500 transition">
              <input type="radio" name="payment_rail" value="paypal" checked class="text-brand-500 focus:ring-brand-500">
              <span class="font-bold text-white flex items-center space-x-1.5"><i data-lucide="credit-card" class="w-4 h-4 text-blue-400"></i><span>PayPal Checkout</span></span>
            </label>
            <label class="flex items-center space-x-2 p-2.5 rounded-lg border border-gray-700 bg-gray-950/60 cursor-pointer hover:border-brand-500 transition">
              <input type="radio" name="payment_rail" value="crypto" class="text-brand-500 focus:ring-brand-500">
              <span class="font-bold text-white flex items-center space-x-1.5"><i data-lucide="coins" class="w-4 h-4 text-emerald-400"></i><span>Crypto (USDC / SOL)</span></span>
            </label>
          </div>
        </div>

        <div id="campaign-checkout-status" class="hidden text-xs p-3 rounded-lg"></div>

        <div class="pt-4 border-t border-gray-800 flex items-center justify-end space-x-3">
          <button type="button" onclick="closeCampaignModal()" class="px-4 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs font-semibold transition">Cancel</button>
          <button type="submit" id="btn-submit-campaign" class="px-5 py-2 rounded-lg bg-gradient-to-r from-brand-600 to-accent-500 hover:from-brand-500 hover:to-accent-400 text-white font-bold text-xs shadow-lg transition flex items-center space-x-1.5">
            <i data-lucide="credit-card" class="w-4 h-4"></i>
            <span>Continue to Payment Checkout</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- TRUST & COMPLIANCE MODAL -->
  <div id="trust-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-gray-900 border border-gray-700 rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl">
      <div class="p-6 border-b border-gray-800 flex items-center justify-between">
        <h3 id="modal-title" class="text-lg font-bold text-white">Trust &amp; Legal</h3>
        <button onclick="closeModal()" class="text-gray-400 hover:text-white p-1 rounded-lg hover:bg-gray-800 transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div id="modal-body" class="p-6 overflow-y-auto space-y-4 text-xs text-gray-300 leading-relaxed">
      </div>
      <div class="p-4 border-t border-gray-800 flex justify-end">
        <button onclick="closeModal()" class="px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition">Close</button>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col space-y-2 pointer-events-none"></div>

  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    let currentOwner = 'tiangolo';
    let currentRepo = 'fastapi';
    let currentBadgeStyle = 'banner';
    let currentTheme = 'dark';
    let currentSponsorPos = 'right';
    let currentMarquee = false;
    let currentHideStars = false;
    let currentHideCi = false;
    let currentSnippetFormat = 'markdown';
    let currentSnippets = null;

    let activeAuthUser = null;
    let maintainerClaimedRepos = [];

    let activeSponsorName = null;
    let sponsorCampaigns = [];

    let directoryData = [];

    // Initialize Lucide Icons
    function updateIcons() {
      if (window.lucide) {
        lucide.createIcons();
      }
    }

    // Trust & Compliance Modals
    const modalTexts = {
      privacy: {
        title: "Privacy Policy",
        html: `
          <p class="font-semibold text-white">Last Updated: October 2026</p>
          <p><strong>1. Information We Collect:</strong> ReadmePay collects publicly available repository metadata from the GitHub REST API (such as star counts, primary programming language, and CI/CD status). For maintainers choosing to connect their GitHub accounts, we temporarily request read-only profile information and collaborator access permissions via the official GitHub OAuth service.</p>
          <p><strong>2. Use of Information:</strong> GitHub OAuth access tokens are used strictly and solely to confirm repository ownership or administrative privileges. We never request access to private code, never modify commit history, and never store repository contents or private user credentials.</p>
          <p><strong>3. Analytics & Cookies:</strong> We do not use third-party behavioral trackers or selling cookies. Badge impression analytics use one-way salted SHA-256 hashes to prevent fraudulent impression manipulation without recording identifiable personal IP histories.</p>
          <p><strong>4. Payout Information:</strong> Maintainer payout destinations (such as PayPal email addresses or public crypto wallet addresses) are stored securely and used exclusively to disburse automated 50% revenue share distributions.</p>
        `
      },
      terms: {
        title: "Terms of Service",
        html: `
          <p class="font-semibold text-white">Last Updated: October 2026</p>
          <p><strong>1. Acceptance:</strong> By accessing ReadmePay or embedding our dynamic SVG badges, maintainers and advertisers agree to these terms.</p>
          <p><strong>2. Maintainer Eligibility:</strong> Repositories may only be claimed by legitimate maintainers possessing verifiable admin or write collaborator permissions verified via GitHub OAuth2 authentication.</p>
          <p><strong>3. Advertising Standards:</strong> All sponsor campaigns must offer safe, legitimate software, developer tools, or developer infrastructure products. Deceptive ads, malware, illegal services, and fraudulent links are strictly prohibited and immediately purged.</p>
          <p><strong>4. Revenue Distribution:</strong> Gross click revenue is partitioned strictly 50/50 between verified repository maintainers and platform operations, settled monthly via PayPal mass disbursements or crypto transfers upon meeting standard disbursement thresholds.</p>
        `
      },
      security: {
        title: "Security & GitHub OAuth Disclosure",
        html: `
          <div class="p-3 bg-brand-950/40 border border-brand-500/30 rounded-lg text-brand-300">
            <strong>Legitimate Developer Verification:</strong> ReadmePay is an open-source monetization tool registered in the official GitHub Developer Directory.
          </div>
          <p><strong>Why We Use GitHub OAuth:</strong> To prevent scammers from maliciously claiming open-source repositories and collecting ad revenue intended for legitimate authors, we authenticate repository administrators using GitHub's official OAuth2 consent screen.</p>
          <p><strong>Minimal Permissions Scope:</strong> We request only the standard <code>read:user</code> and <code>repo</code> permissions needed to verify collaborator status against GitHub's permissions API endpoint. We never request or require permission to write code or modify repository settings.</p>
          <p><strong>Encryption Standards:</strong> All web endpoints use modern TLS 1.3 cryptographic suites with automated certificate rotation.</p>
        `
      }
    };

    function openModal(type) {
      const data = modalTexts[type];
      if (!data) return;
      document.getElementById('modal-title').innerText = data.title;
      document.getElementById('modal-body').innerHTML = data.html;
      document.getElementById('trust-modal').classList.remove('hidden');
      updateIcons();
    }

    function closeModal() {
      document.getElementById('trust-modal').classList.add('hidden');
    }

    function showToast(msg) {
      const c = document.getElementById('toast-container');
      if (!c) return;
      const t = document.createElement('div');
      t.className = 'bg-gray-900 border border-brand-500/50 text-white text-xs px-4 py-2.5 rounded-xl shadow-2xl flex items-center space-x-2 transition-all duration-300 opacity-0 translate-y-2';
      t.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4 text-brand-400"></i><span>${msg}</span>`;
      c.appendChild(t);
      updateIcons();
      setTimeout(() => {
        t.classList.remove('opacity-0', 'translate-y-2');
      }, 10);
      setTimeout(() => {
        t.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => t.remove(), 300);
      }, 3500);
    }

    // Tab Navigation
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      const activeContent = document.getElementById(`tab-${tabId}`);
      if (activeContent) activeContent.classList.remove('hidden');

      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('tab-active'));
      const activeNav = document.getElementById(`nav-${tabId}`);
      if (activeNav) activeNav.classList.add('tab-active');

      if (tabId === 'directory') loadDirectory();
      if (tabId === 'sponsors') loadSponsors();
      if (tabId === 'revenue') checkMaintainerAuthSession();

      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateIcons();
    }

    function scrollToGallery() {
      switchTab('home');
      setTimeout(() => {
        const el = document.getElementById('badge-showcase-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 50);
    }

    // Maintainer Studio Navigation
    function openMaintainerStudio(style, theme) {
      if (style) currentBadgeStyle = style;
      if (theme) currentTheme = theme;
      switchTab('revenue');
      if (activeAuthUser) {
        setTimeout(() => {
          const sandbox = document.getElementById('studio-sandbox');
          if (sandbox) sandbox.scrollIntoView({ behavior: 'smooth' });
          setStudioStyle(currentBadgeStyle);
          setStudioTheme(currentTheme);
        }, 100);
      }
    }

    function copySnippetForStyle(style, theme) {
      const base = window.location.origin;
      const owner = currentOwner || 'tiangolo';
      const repo = currentRepo || 'fastapi';
      const params = new URLSearchParams();
      if (style && style !== 'banner') params.append('style', style);
      if (theme && theme !== 'dark') params.append('theme', theme);
      const q = params.toString() ? `?${params.toString()}` : '';
      const badgeUrl = `${base}/badge/${owner}/${repo}.svg${q}`;
      const clickUrl = (currentSnippets && currentSnippets.click_url && currentSnippets.click_url.includes('/click/')) 
        ? `${base}/click/active/${currentSnippets.repo_id || 1}` 
        : `${base}/maintainers/claim?repo=${owner}/${repo}`;
      const md = `[![Sponsorship Badge](${badgeUrl})](${clickUrl})`;
      navigator.clipboard.writeText(md).then(() => {
        showToast(`Copied Markdown for ${style} style!`);
      }).catch(() => {
        prompt('Copy Markdown:', md);
      });
    }

    // =========================================================================
    // MAINTAINER AUTHENTICATION & SESSION
    // =========================================================================
    async function checkMaintainerAuthSession() {
      try {
        const res = await fetch('/api/auth/github/user');
        if (res.ok) {
          const data = await res.json();
          if (data.authenticated && data.username) {
            activeAuthUser = data.username;
            maintainerClaimedRepos = data.repos || [];

            // Show authenticated view, hide lock gate
            document.getElementById('maintainer-auth-gate').classList.add('hidden');
            document.getElementById('maintainer-authenticated-view').classList.remove('hidden');

            const nameEl = document.getElementById('auth-maintainer-name');
            if (nameEl) nameEl.innerText = `@${data.username}`;
            const navLabel = document.getElementById('nav-user-label');
            if (navLabel) navLabel.innerText = `@${data.username}`;

            // Update KPI cards from summary
            if (data.summary) {
              const kpiMaint = document.getElementById('kpi-maintainer');
              if (kpiMaint) kpiMaint.innerText = `$${(data.summary.total_earnings || 0).toFixed(2)}`;
              const kpiGross = document.getElementById('kpi-gross');
              if (kpiGross) kpiGross.innerText = `$${(data.summary.gross_revenue || 0).toFixed(2)}`;
              const kpiClicks = document.getElementById('kpi-clicks');
              if (kpiClicks) kpiClicks.innerText = `${(data.summary.total_clicks || 0).toLocaleString()} Clicks`;
              const countEl = document.getElementById('maintainer-repo-count');
              if (countEl) countEl.innerText = `${data.summary.claimed_repos_count || 0} of ${data.summary.total_repos || 0}`;
            }

            // Populate repo selectors
            populateMaintainerRepoSelectors();
            renderMaintainerPortfolioTable(maintainerClaimedRepos);
            updateIcons();
            return;
          }
        }
      } catch (err) {
        console.error("Maintainer auth check error:", err);
      }

      // Unauthenticated
      activeAuthUser = null;
      document.getElementById('maintainer-auth-gate').classList.remove('hidden');
      document.getElementById('maintainer-authenticated-view').classList.add('hidden');
      const navLabel = document.getElementById('nav-user-label');
      if (navLabel) navLabel.innerText = "Maintainer Login";
      updateIcons();
    }

    function populateMaintainerRepoSelectors() {
      const studioSel = document.getElementById('studio-repo-selector');
      const dashSel = document.getElementById('select-claimed-repos');
      if (!studioSel || !dashSel) return;

      studioSel.innerHTML = '';
      dashSel.innerHTML = '';

      if (maintainerClaimedRepos.length > 0) {
        maintainerClaimedRepos.forEach(r => {
          const opt1 = document.createElement('option');
          opt1.value = `${r.owner}/${r.name}`;
          opt1.innerText = `${r.owner}/${r.name} (${(r.stars || 0).toLocaleString()} ★)`;
          studioSel.appendChild(opt1);

          const opt2 = document.createElement('option');
          opt2.value = `${r.owner}/${r.name}`;
          opt2.innerText = `${r.owner}/${r.name} (${(r.stars || 0).toLocaleString()} ★)${r.claimed ? ' ✓' : ' (Paused)'}`;
          dashSel.appendChild(opt2);
        });

        // Set inputs to first repo
        const first = maintainerClaimedRepos[0];
        document.getElementById('input-owner').value = first.owner;
        document.getElementById('input-repo').value = first.name;
        renderStudioBadge();
      } else {
        const opt = document.createElement('option');
        opt.value = '';
        opt.innerText = 'No public repos found (Click Enroll All)';
        studioSel.appendChild(opt);
        dashSel.appendChild(opt.cloneNode(true));
      }
    }

    function onStudioRepoSelect(fullRepo) {
      if (!fullRepo || !fullRepo.includes('/')) return;
      const parts = fullRepo.split('/');
      document.getElementById('input-owner').value = parts[0];
      document.getElementById('input-repo').value = parts[1];
      renderStudioBadge();
    }

    function loginWithGitHubForDashboard() {
      window.location.href = `/api/auth/github/login`;
    }

    async function claimAllPublicRepos() {
      const btn = document.getElementById('btn-claim-all-public');
      const icon = document.getElementById('icon-claim-all');
      if (btn) btn.disabled = true;
      if (icon) icon.classList.add('animate-spin');

      try {
        const res = await fetch('/api/maintainers/claim-all', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ payout_address: document.getElementById('input-global-payout')?.value || null })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`✓ Enrolled ${data.claimed_count} repositories into your portfolio!`);
          checkMaintainerAuthSession();
        } else {
          showToast(`Error: ${data.detail || 'Could not enroll repositories'}`);
        }
      } catch (err) {
        showToast(`Enrollment error: ${err.message}`);
      } finally {
        if (btn) btn.disabled = false;
        if (icon) icon.classList.remove('animate-spin');
      }
    }

    function renderMaintainerPortfolioTable(repos) {
      const tbody = document.getElementById('maintainer-portfolio-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!repos || repos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="px-4 py-8 text-center text-gray-500">No public repositories claimed yet. Click "Enroll All Public Repos" above.</td></tr>`;
        return;
      }

      repos.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-900/50 transition';
        const isClaimed = r.claimed;
        tr.innerHTML = `
          <td class="px-4 py-3 font-medium text-white flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full ${isClaimed ? 'bg-brand-500' : 'bg-gray-600'}"></span>
            <span class="font-mono">${r.owner}/${r.name}</span>
          </td>
          <td class="px-4 py-3 text-gray-400 font-mono">${(r.stars || 0).toLocaleString()} ★</td>
          <td class="px-4 py-3">
            <button onclick="toggleRepoClaim(${r.id}, ${!isClaimed})" class="px-2.5 py-1 rounded text-[11px] font-bold ${isClaimed ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30' : 'bg-gray-800 text-gray-400 border border-gray-700'} transition">
              ${isClaimed ? 'Active (Monetized)' : 'Paused'}
            </button>
          </td>
          <td class="px-4 py-3 text-brand-300 font-mono font-bold">$${(r.earnings || 0).toFixed(2)}</td>
          <td class="px-4 py-3 text-gray-400 font-mono">${(r.clicks || 0).toLocaleString()}</td>
          <td class="px-4 py-3 text-right">
            <button onclick="quickCopyRepoSnippet('${r.owner}', '${r.name}', ${r.id})" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white border border-gray-700 text-[11px] font-semibold transition flex items-center space-x-1 inline-flex">
              <i data-lucide="copy" class="w-3 h-3"></i>
              <span>Snippet</span>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
      updateIcons();
    }

    async function toggleRepoClaim(repoId, newStatus) {
      try {
        const res = await fetch('/api/maintainers/toggle-claim', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ repo_id: repoId, claimed: newStatus })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(data.message || 'Repository status updated.');
          checkMaintainerAuthSession();
        } else {
          showToast(`Error: ${data.detail || 'Toggle failed'}`);
        }
      } catch (err) {
        showToast(`Toggle error: ${err.message}`);
      }
    }

    async function saveGlobalPayout() {
      const payoutVal = document.getElementById('input-global-payout')?.value?.trim();
      if (!payoutVal) {
        showToast('Please enter a valid payout address.');
        return;
      }
      try {
        const res = await fetch('/api/maintainers/payout-address', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ payout_address: payoutVal })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`Payout address saved to ${data.updated_repositories} repositories!`);
          checkMaintainerAuthSession();
        } else {
          showToast(`Error: ${data.detail || 'Failed to update payout'}`);
        }
      } catch (err) {
        showToast(`Save payout error: ${err.message}`);
      }
    }

    function quickCopyRepoSnippet(owner, repo, repoId) {
      const base = window.location.origin;
      const badgeUrl = `${base}/badge/${owner}/${repo}.svg`;
      const clickUrl = `${base}/click/active/${repoId}`;
      const md = `[![Sponsorship Badge](${badgeUrl})](${clickUrl})`;
      navigator.clipboard.writeText(md).then(() => {
        showToast(`Copied README badge markdown for ${owner}/${repo}!`);
      });
    }

    // =========================================================================
    // SPONSOR AUTHENTICATION & DASHBOARD
    // =========================================================================
    async function loadSponsors() {
      await checkSponsorAuthSession();
      loadPublicSponsorsCatalog();
    }

    async function checkSponsorAuthSession() {
      try {
        const res = await fetch('/api/auth/sponsor/user');
        if (res.ok) {
          const data = await res.json();
          if (data.authenticated && data.sponsor_name) {
            activeSponsorName = data.sponsor_name;
            sponsorCampaigns = data.campaigns || [];

            // Show authenticated view, hide login gate
            document.getElementById('sponsor-login-gate').classList.add('hidden');
            document.getElementById('sponsor-authenticated-view').classList.remove('hidden');

            const nameEl = document.getElementById('auth-sponsor-name');
            if (nameEl) nameEl.innerText = data.sponsor_name;
            const navLabel = document.getElementById('nav-sponsor-label');
            if (navLabel) navLabel.innerText = `Sponsor: ${data.sponsor_name}`;

            // Update KPI summary cards
            if (data.summary) {
              const kpiCamp = document.getElementById('sp-kpi-campaigns');
              if (kpiCamp) kpiCamp.innerText = data.summary.total_campaigns;
              const kpiBudget = document.getElementById('sp-kpi-budget');
              if (kpiBudget) kpiBudget.innerText = `$${(data.summary.remaining_budget || 0).toFixed(2)}`;
              const kpiClicks = document.getElementById('sp-kpi-clicks');
              if (kpiClicks) kpiClicks.innerText = `${(data.summary.total_clicks || 0).toLocaleString()} Clicks`;
              const kpiCtr = document.getElementById('sp-kpi-ctr');
              if (kpiCtr) kpiCtr.innerText = `Avg CTR: ${(data.summary.avg_ctr || 0).toFixed(1)}%`;
              const kpiSpent = document.getElementById('sp-kpi-spent');
              if (kpiSpent) kpiSpent.innerText = `$${(data.summary.total_spent || 0).toFixed(2)}`;
            }

            renderSponsorPersonalCampaigns(sponsorCampaigns);
            updateIcons();
            return;
          }
        }
      } catch (err) {
        console.error("Sponsor auth check error:", err);
      }

      // Unauthenticated
      activeSponsorName = null;
      document.getElementById('sponsor-login-gate').classList.remove('hidden');
      document.getElementById('sponsor-authenticated-view').classList.add('hidden');
      const navLabel = document.getElementById('nav-sponsor-label');
      if (navLabel) navLabel.innerText = "Sponsor Portal";
      updateIcons();
    }

    async function handleSponsorLoginForm(e) {
      e.preventDefault();
      const val = document.getElementById('input-sponsor-name')?.value?.trim();
      if (!val) return;
      await executeSponsorLogin(val);
    }

    function quickSponsorLogin(name) {
      executeSponsorLogin(name);
    }

    async function executeSponsorLogin(sponsorName) {
      const btn = document.getElementById('btn-sponsor-login');
      if (btn) btn.disabled = true;

      try {
        const res = await fetch('/api/auth/sponsor/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sponsor_name: sponsorName })
        });
        const data = await res.json();
        if (res.ok) {
          showToast(`Signed in as sponsor '${sponsorName}'`);
          checkSponsorAuthSession();
        } else {
          showToast(`Error: ${data.detail || 'Could not sign in'}`);
        }
      } catch (err) {
        showToast(`Sign in error: ${err.message}`);
      } finally {
        if (btn) btn.disabled = false;
      }
    }

    async function logoutSponsor() {
      try {
        await fetch('/api/auth/sponsor/logout', { method: 'POST' });
        showToast('Signed out of sponsor account.');
        checkSponsorAuthSession();
      } catch (err) {
        console.error("Logout error:", err);
      }
    }

    function renderSponsorPersonalCampaigns(campaigns) {
      const grid = document.getElementById('sponsor-personal-campaigns-grid');
      if (!grid) return;
      grid.innerHTML = '';

      if (!campaigns || campaigns.length === 0) {
        grid.innerHTML = `<div class="col-span-2 p-8 text-center text-gray-500 glass-card rounded-xl">No campaigns found under this brand name. Click "New Campaign" to create your first ad!</div>`;
        return;
      }

      campaigns.forEach(c => {
        const pct = c.total_budget > 0 ? Math.round((c.remaining_budget / c.total_budget) * 100) : 100;
        const isActive = c.is_active && c.remaining_budget > 0;
        grid.innerHTML += `
          <div class="glass-card rounded-xl p-5 space-y-3.5 border ${isActive ? 'border-brand-500/30' : 'border-gray-800'}">
            <div class="flex items-center justify-between">
              <span class="text-xs uppercase font-bold px-2 py-0.5 rounded bg-accent-500/10 text-accent-400 border border-accent-500/20">${c.target_language}</span>
              <span class="text-xs font-semibold ${isActive ? 'text-brand-400' : 'text-gray-500'} font-mono">${isActive ? 'Active' : 'Depleted'}</span>
            </div>
            <div>
              <h4 class="text-base font-bold text-white">${c.sponsor_name}</h4>
              <p class="text-xs text-gray-300 mt-1">${c.headline}</p>
            </div>
            <div class="space-y-1">
              <div class="flex justify-between text-[11px] text-gray-400 font-mono">
                <span>Remaining Budget</span>
                <span>$${c.remaining_budget.toFixed(2)} / $${c.total_budget.toFixed(2)}</span>
              </div>
              <div class="w-full bg-gray-800 rounded-full h-1.5 overflow-hidden">
                <div class="bg-brand-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>
            <div class="flex items-center justify-between pt-2 border-t border-gray-800 text-[11px] text-gray-400 font-mono">
              <span>Clicks: ${c.clicks_count}</span>
              <span>CTR: ${c.ctr}%</span>
              <span>$${c.cpc.toFixed(2)} CPC</span>
            </div>
          </div>
        `;
      });
      updateIcons();
    }

    async function loadPublicSponsorsCatalog() {
      try {
        const res = await fetch('/api/inventory/ads');
        if (res.ok) {
          const data = await res.json();
          const grid = document.getElementById('sponsors-grid');
          if (!grid) return;
          grid.innerHTML = '';

          data.ads.forEach(ad => {
            const pct = ad.total_budget > 0 ? Math.round((ad.remaining_budget / ad.total_budget) * 100) : 100;
            grid.innerHTML += `
              <div class="glass-card rounded-xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs uppercase font-bold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">${ad.target_language}</span>
                  <span class="text-xs font-semibold text-brand-400">$${ad.cpc.toFixed(2)} CPC</span>
                </div>
                <div>
                  <h4 class="text-base font-bold text-white">${ad.sponsor_name}</h4>
                  <p class="text-xs text-gray-400 mt-1">${ad.headline}</p>
                </div>
                <div class="space-y-1">
                  <div class="flex justify-between text-[11px] text-gray-500 font-mono">
                    <span>Budget Status</span>
                    <span>$${ad.remaining_budget.toFixed(2)} Remaining</span>
                  </div>
                  <div class="w-full bg-gray-800 rounded-full h-1.5 overflow-hidden">
                    <div class="bg-brand-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
                  </div>
                </div>
              </div>
            `;
          });
          updateIcons();
        }
      } catch (err) {
        console.error("Public sponsors catalog error:", err);
      }
    }

    // Campaign Modal & Checkout
    function openCreateCampaignModal() {
      document.getElementById('modal-campaign').classList.remove('hidden');
      updateIcons();
    }

    function closeCampaignModal() {
      document.getElementById('modal-campaign').classList.add('hidden');
    }

    async function submitNewCampaign(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-submit-campaign');
      const statusBox = document.getElementById('campaign-checkout-status');
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Processing...</span>`;
      statusBox.classList.add('hidden');

      const payload = {
        sponsor_name: document.getElementById('ad-sponsor-name').value.trim(),
        headline: document.getElementById('ad-headline').value.trim(),
        cta_text: document.getElementById('ad-cta-text').value.trim(),
        click_url: document.getElementById('ad-click-url').value.trim(),
        target_language: document.getElementById('ad-target-lang').value,
        target_repo_name: document.getElementById('ad-target-repo').value.trim() || null,
        initial_budget: parseFloat(document.getElementById('ad-budget').value),
        cost_per_click: parseFloat(document.getElementById('ad-cpc').value),
      };

      const rail = document.querySelector('input[name="payment_rail"]:checked')?.value || 'paypal';

      try {
        const res = await fetch('/api/inventory/ads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Could not register campaign.');
        }

        const adData = await res.json();
        const adId = adData.ad_id;

        if (rail === 'paypal') {
          const resPaypal = await fetch('/api/billing/paypal/create-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ad_id: adId, amount: payload.initial_budget, currency: 'USD' })
          });
          if (!resPaypal.ok) {
            const errP = await resPaypal.json();
            throw new Error(errP.detail || 'PayPal checkout initialization failed.');
          }
          const paypalOrder = await resPaypal.json();
          statusBox.className = 'text-xs p-3 rounded-lg border border-brand-500/40 bg-brand-950/40 text-brand-200';
          statusBox.innerHTML = `Order initialized (ID: ${paypalOrder.order_id}). Confirming payment capture...`;
          statusBox.classList.remove('hidden');

          const resCapture = await fetch('/api/billing/paypal/capture-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order_id: paypalOrder.order_id, ad_id: adId })
          });
          if (resCapture.ok) {
            statusBox.innerHTML = `✓ Payment captured successfully! Campaign is now live across matching READMEs.`;
            showToast(`Campaign '${payload.sponsor_name}' activated!`);
            setTimeout(() => {
              closeCampaignModal();
              loadSponsors();
            }, 1200);
          }
        } else {
          const resCrypto = await fetch('/api/billing/crypto/create-invoice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ad_id: adId, amount_usd: payload.initial_budget, crypto_currency: 'USDC' })
          });
          if (!resCrypto.ok) {
            const errCrypto = await resCrypto.json();
            throw new Error(errCrypto.detail || 'Crypto invoice initialization failed.');
          }
          const invoiceData = await resCrypto.json();
          statusBox.className = 'text-xs p-4 rounded-xl border border-brand-500/40 bg-brand-950/40 text-brand-200 space-y-2';
          statusBox.innerHTML = `
            <div class="font-bold text-sm text-white">Deposit ${invoiceData.pay_amount} ${invoiceData.pay_currency.toUpperCase()} to activate:</div>
            <div class="bg-gray-950 p-2 rounded font-mono text-[11px] select-all break-all text-cyan-300">${invoiceData.pay_address}</div>
            <p class="text-[11px] text-gray-400">Campaign activates automatically as soon as payment is confirmed on-chain.</p>
          `;
          statusBox.classList.remove('hidden');
          loadSponsors();
        }
      } catch (err) {
        statusBox.className = 'text-xs p-3 rounded-lg border border-rose-500/40 bg-rose-950/40 text-rose-200';
        statusBox.innerText = `Error: ${err.message}`;
        statusBox.classList.remove('hidden');
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="credit-card" class="w-4 h-4"></i><span>Continue to Payment Checkout</span>`;
        updateIcons();
      }
    }

    // =========================================================================
    // BADGE STUDIO & RENDERING ENGINE
    // =========================================================================
    function setStudioStyle(style) {
      currentBadgeStyle = style;
      const styles = ['banner', 'linear', 'spotlight', 'compact', 'backer', 'goal', 'shield'];
      styles.forEach(s => {
        const btn = document.getElementById(`btn-style-${s}`);
        if (btn) {
          if (s === style) {
            btn.className = 'px-2.5 py-1 text-xs rounded font-medium text-brand-300 bg-brand-500/15 border border-brand-500/30 transition flex items-center space-x-1';
          } else {
            btn.className = 'px-2.5 py-1 text-xs rounded font-medium text-gray-400 hover:text-gray-200 transition flex items-center space-x-1';
          }
        }
      });
      renderStudioBadge();
    }

    function setStudioTheme(theme) {
      currentTheme = theme;
      ['dark', 'cyberpunk', 'emerald', 'light', 'linear', 'dracula', 'nord', 'monokai', 'synthwave'].forEach(t => {
        const btn = document.getElementById(`theme-btn-${t}`);
        if (btn) {
          if (t === theme) {
            btn.className = 'px-2 py-0.5 rounded text-[11px] font-medium bg-brand-500/20 text-brand-300 border border-brand-500/30';
          } else {
            btn.className = 'px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-white';
          }
        }
      });
      renderStudioBadge();
    }

    function setStudioSponsorPos(pos) {
      currentSponsorPos = pos;
      ['right', 'left'].forEach(p => {
        const btn = document.getElementById(`pos-btn-${p}`);
        if (btn) {
          if (p === pos) {
            btn.className = 'px-2 py-0.5 rounded text-[11px] font-medium bg-brand-500/20 text-brand-300 border border-brand-500/30';
          } else {
            btn.className = 'px-2 py-0.5 rounded text-[11px] font-medium text-gray-400 hover:text-white';
          }
        }
      });
      renderStudioBadge();
    }

    function toggleStudioMarquee() {
      const chk = document.getElementById('check-marquee');
      currentMarquee = chk ? chk.checked : false;
      renderStudioBadge();
    }

    function toggleStudioStats() {
      const chkStars = document.getElementById('check-hide-stars');
      const chkCi = document.getElementById('check-hide-ci');
      currentHideStars = chkStars ? chkStars.checked : false;
      currentHideCi = chkCi ? chkCi.checked : false;
      renderStudioBadge();
    }

    function buildBadgeQueryString() {
      const params = new URLSearchParams();
      if (currentBadgeStyle !== 'banner') params.append('style', currentBadgeStyle);
      if (currentTheme !== 'dark') params.append('theme', currentTheme);
      if (currentSponsorPos === 'left') params.append('sponsor_pos', 'left');
      if (currentMarquee) params.append('marquee', 'true');
      if (currentHideStars) params.append('hide_stars', 'true');
      if (currentHideCi) params.append('hide_ci', 'true');
      const q = params.toString();
      return q ? `?${q}` : '';
    }

    async function renderStudioBadge() {
      const owner = document.getElementById('input-owner').value.trim();
      const repo = document.getElementById('input-repo').value.trim();
      if (!owner || !repo) return;

      currentOwner = owner;
      currentRepo = repo;

      const refreshIcon = document.getElementById('icon-refresh');
      if (refreshIcon) refreshIcon.classList.add('animate-spin');

      const img = document.getElementById('badge-preview-img');
      const timestamp = new Date().getTime();
      const qStr = buildBadgeQueryString();
      const sep = qStr ? '&' : '?';
      img.src = `/badge/${owner}/${repo}.svg${qStr}${sep}t=${timestamp}`;

      try {
        const res = await fetch(`/api/repos/${owner}/${repo}/preview`);
        if (res.ok) {
          const data = await res.json();
          currentSnippets = data.snippets;
          updateSnippetBox();

          document.getElementById('preview-stars').innerHTML = `<i data-lucide="star" class="w-3.5 h-3.5 text-yellow-400"></i><span>${(data.stars || 0).toLocaleString()} stars</span>`;
          document.getElementById('preview-lang').innerHTML = `<i data-lucide="code" class="w-3.5 h-3.5 text-cyan-400"></i><span>${data.primary_language || 'General'}</span>`;
          
          const sponsorText = data.matched_ad ? `${data.matched_ad.sponsor_name} ($${data.matched_ad.cpc} CPC)` : 'Platform Onboarding';
          document.getElementById('preview-sponsor').innerHTML = `<i data-lucide="heart" class="w-3.5 h-3.5 text-pink-400"></i><span>${sponsorText}</span>`;

          const testBtn = document.getElementById('btn-test-click');
          if (testBtn) testBtn.href = data.click_url;
        } else {
          updateSnippetBox();
        }
      } catch (err) {
        console.error("Preview fetch error:", err);
      } finally {
        if (refreshIcon) refreshIcon.classList.remove('animate-spin');
        updateIcons();
      }
    }

    function setSnippetTab(format) {
      currentSnippetFormat = format;
      document.querySelectorAll('.snip-tab-btn').forEach(btn => {
        btn.className = 'snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-gray-400 hover:text-gray-200';
      });
      const activeBtn = document.getElementById(`btn-snip-${format}`);
      if (activeBtn) {
        activeBtn.className = 'snip-tab-btn px-2.5 py-1 text-xs rounded-md font-medium text-brand-300 bg-brand-500/10 border border-brand-500/30';
      }
      updateSnippetBox();
    }

    function updateSnippetBox() {
      const box = document.getElementById('snippet-code-box');
      if (!currentSnippets) return;

      const base = window.location.origin;
      const qStr = buildBadgeQueryString();
      const badgeUrl = `${base}/badge/${currentOwner}/${currentRepo}.svg${qStr}`;
      const clickUrl = (currentSnippets.click_url && currentSnippets.click_url.includes('/click/')) 
        ? `${base}/click/active/${currentSnippets.repo_id || 1}` 
        : `${base}/maintainers/claim?repo=${currentOwner}/${currentRepo}`;

      const markdown = `[![Sponsorship Badge](${badgeUrl})](${clickUrl})`;
      const shieldsIo = `[![Sponsor](https://img.shields.io/endpoint?url=${base}/badge/${currentOwner}/${currentRepo}/shield.json)](${clickUrl})`;
      const html = `<a href="${clickUrl}"><img src="${badgeUrl}" alt="Sponsorship Badge" /></a>`;
      const rst = `.. image:: ${badgeUrl}\n   :target: ${clickUrl}\n   :alt: Sponsorship Badge`;

      if (currentSnippetFormat === 'markdown') {
        box.value = markdown;
      } else if (currentSnippetFormat === 'shieldsio') {
        box.value = shieldsIo;
      } else if (currentSnippetFormat === 'html') {
        box.value = html;
      } else if (currentSnippetFormat === 'rst') {
        box.value = rst;
      } else if (currentSnippetFormat === 'urls') {
        box.value = `Badge SVG: ${badgeUrl}\nShields.io JSON: ${base}/badge/${currentOwner}/${currentRepo}/shield.json\nClick Redirect: ${clickUrl}`;
      }
    }

    function copyCurrentSnippet() {
      const box = document.getElementById('snippet-code-box');
      if (!box.value) return;
      navigator.clipboard.writeText(box.value).then(() => {
        const btnText = document.getElementById('copy-btn-text');
        btnText.innerText = 'Copied!';
        setTimeout(() => { btnText.innerText = 'Copy Snippet'; }, 2000);
      });
    }

    function handlePreviewError() {
      document.getElementById('preview-meta').innerHTML = `<span class="text-rose-400 font-semibold">Repository not found or network error.</span>`;
    }

    // =========================================================================
    // DIRECTORY TABLE
    // =========================================================================
    async function loadDirectory() {
      try {
        const res = await fetch('/api/inventory/repos');
        if (res.ok) {
          const data = await res.json();
          directoryData = data.repositories || [];
          renderDirectoryTable(directoryData);
        }
      } catch (err) {
        console.error("Directory load error:", err);
      }
    }

    function renderDirectoryTable(repos) {
      const tbody = document.getElementById('directory-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!repos || repos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="px-4 py-8 text-center text-gray-500">No repositories found.</td></tr>`;
        return;
      }

      repos.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-900/50 transition';
        const isClaimed = r.claimed;
        tr.innerHTML = `
          <td class="px-4 py-3 font-medium text-white flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full ${isClaimed ? 'bg-brand-500' : 'bg-gray-600'}"></span>
            <span class="font-mono">${r.full_name}</span>
          </td>
          <td class="px-4 py-3 text-gray-400 font-mono">${(r.stars || 0).toLocaleString()} ★</td>
          <td class="px-4 py-3 text-cyan-300 font-mono">${r.primary_language || 'General'}</td>
          <td class="px-4 py-3">
            <span class="px-2 py-0.5 rounded text-[11px] font-bold ${isClaimed ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30' : 'bg-gray-800 text-gray-400 border border-gray-700'}">
              ${isClaimed ? 'Claimed' : 'Unclaimed'}
            </span>
          </td>
          <td class="px-4 py-3 text-right">
            <a href="/badge/${r.full_name}.svg" target="_blank" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white border border-gray-700 text-[11px] font-semibold transition inline-flex items-center space-x-1">
              <i data-lucide="eye" class="w-3 h-3"></i>
              <span>View Badge</span>
            </a>
          </td>
        `;
        tbody.appendChild(tr);
      });
      updateIcons();
    }

    function filterDirectoryTable() {
      const q = document.getElementById('dir-search-input').value.toLowerCase();
      const filtered = directoryData.filter(r => r.full_name.toLowerCase().includes(q) || (r.primary_language && r.primary_language.toLowerCase().includes(q)));
      renderDirectoryTable(filtered);
    }

    // Auto-init on load
    document.addEventListener('DOMContentLoaded', () => {
      updateIcons();
      const params = new URLSearchParams(window.location.search);
      const tab = params.get('tab');
      const owner = params.get('owner');
      const repo = params.get('repo');
      const claim = params.get('claim');

      if (owner && repo) {
        document.getElementById('input-owner').value = owner;
        document.getElementById('input-repo').value = repo;
        const targetRepoInput = document.getElementById('ad-target-repo');
        if (targetRepoInput) targetRepoInput.value = `${owner}/${repo}`;
      }

      // Check sessions in parallel
      checkMaintainerAuthSession();
      checkSponsorAuthSession();

      if (tab) {
        switchTab(tab);
      } else if (claim) {
        switchTab('revenue');
      } else if (window.location.pathname.includes('/sponsor') || params.get('sponsor')) {
        switchTab('sponsors');
        if (params.get('repo') || (owner && repo)) {
          openCreateCampaignModal();
        }
      } else {
        switchTab('home');
      }

      renderStudioBadge();
    });
  </script>
</body>
</html>
'''

target_path = Path("app/templates/index.html")
target_path.write_text(content, encoding="utf-8")
print(f"Successfully generated {target_path} ({len(content)} bytes)")
