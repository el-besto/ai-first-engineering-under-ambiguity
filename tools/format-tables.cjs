#!/usr/bin/env node

const { execSync } = require('child_process');
const { readFileSync, writeFileSync, readdirSync, statSync } = require('fs');
const { join } = require('path');

function getAllMarkdownFiles(dir, fileList = []) {
  const files = readdirSync(dir);
  const skipDirs = new Set([
    'node_modules',
    '.git',
    '.venv',
    'venv',
    'env',
    '.pytest_cache',
    '.ruff_cache',
    '.mypy_cache',
    '.pyright',
    '.tox',
    '.ipynb_checkpoints',
    '.cache',
    '.local',
    '.idea',
    '.claude',
    '.scratch',
    'build',
    'dist',
    'out',
    'logs'
  ]);

  files.forEach(file => {
    const filePath = join(dir, file);
    const stat = statSync(filePath);

    if (stat.isDirectory()) {
      if (!skipDirs.has(file) && !file.endsWith('.egg-info')) {
        getAllMarkdownFiles(filePath, fileList);
      }
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  });

  return fileList;
}

function formatTables() {
  const files =
    process.argv.length > 2
      ? process.argv.slice(2).filter(file => file.endsWith('.md'))
      : getAllMarkdownFiles('.');

  let processedCount = 0;
  let errorCount = 0;

  for (const file of files) {
    try {
      const content = readFileSync(file, 'utf8');
      let formatted = execSync('npx --yes markdown-table-prettify', {
        input: content,
        encoding: 'utf8'
      });

      if (!formatted.endsWith('\n')) {
        formatted += '\n';
      }

      if (formatted !== content) {
        writeFileSync(file, formatted, 'utf8');
        processedCount++;
      }
    } catch (error) {
      console.error(`Error processing ${file}:`, error.message);
      errorCount++;
    }
  }

  if (processedCount > 0) {
    console.log(`Formatted tables in ${processedCount} file(s).`);
  }

  if (errorCount > 0) {
    process.exit(1);
  }
}

formatTables();
