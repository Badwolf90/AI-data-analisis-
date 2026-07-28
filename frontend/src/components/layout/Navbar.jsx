import React from 'react';
import { Search, Bell, Command, Moon, Sun, Shield, FolderGit2 } from 'lucide-react';

export default function Navbar({ activeTabTitle }) {
  return (
    <header className="h-16 glass-panel border-b border-zinc-800/80 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Title & Path */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-xs text-zinc-400">
          <FolderGit2 className="w-4 h-4 text-zinc-500" />
          <span>workspace</span>
          <span>/</span>
          <span className="font-semibold text-zinc-200 capitalize">{activeTabTitle}</span>
        </div>
      </div>

      {/* Action Controls */}
      <div className="flex items-center gap-4">
        {/* Command Palette Trigger */}
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search datasets, models, experiments..."
            className="w-72 glass-input pl-9 pr-12 py-1.5 text-xs"
          />
          <div className="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-zinc-800 text-[10px] text-zinc-400 border border-zinc-700 font-mono">
            <Command className="w-3 h-3" />
            <span>K</span>
          </div>
        </div>

        {/* Notifications */}
        <button className="relative p-2 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-cyan-400" />
        </button>

        {/* Dark Mode Toggle Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">
          <Moon className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-[11px] font-medium">Obsidian Dark</span>
        </div>
      </div>
    </header>
  );
}
