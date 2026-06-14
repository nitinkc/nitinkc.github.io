// @ts-check
import { readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

const docsRoot = resolve('src/content/docs');
const sidebarSections = readdirSync(docsRoot, { withFileTypes: true })
	.filter((entry) => entry.isDirectory())
	.map((entry) => entry.name)
	.sort((a, b) => a.localeCompare(b))
	.map((directory) => ({
		label: directory
			.replace(/[-_]/g, ' ')
			.replace(/([a-z])([A-Z])/g, '$1 $2')
			.replace(/\b\w/g, (char) => char.toUpperCase()),
		items: [{ autogenerate: { directory } }],
	}));

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
			sidebar: sidebarSections,
		}),
		mermaid({
			theme: 'forest',
			autoTheme: true,
		}),
	],
});