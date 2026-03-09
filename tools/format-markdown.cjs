#!/usr/bin/env node

const { execSync } = require('child_process');
const { join } = require('path');
const { readdirSync, statSync } = require('fs');

function getAllMarkdownFilesInDir(dir, fileList = []) {
  try {
    const items = readdirSync(dir);

    for (const item of items) {
      const fullPath = join(dir, item);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        getAllMarkdownFilesInDir(fullPath, fileList);
      } else if (item.endsWith('.md')) {
        fileList.push(fullPath);
      }
    }
  } catch {
    // Skip directories we cannot read.
  }

  return fileList;
}

function getModifiedMarkdownFiles() {
  try {
    const output = execSync('git status --porcelain', { encoding: 'utf8' });
    const files = [];

    output
      .split('\n')
      .filter(line => line.trim())
      .forEach(line => {
        const match = line.match(/^(?:\?\?|.M|M.|MM|A.)\s+(.+)$/);

        if (!match) {
          return;
        }

        const path = match[1];

        try {
          const stat = statSync(path);

          if (stat.isDirectory()) {
            files.push(...getAllMarkdownFilesInDir(path));
          } else if (path.endsWith('.md')) {
            files.push(path);
          }
        } catch {
          // Skip deleted or transient paths.
        }
      });

    return files;
  } catch {
    return null;
  }
}

function formatMarkdown() {
  const args = process.argv.slice(2);
  const formatAll = args.includes('--all');
  const explicitFiles = args.filter(arg => !arg.startsWith('-'));

  let filesToFormat;

  if (explicitFiles.length > 0) {
    filesToFormat = explicitFiles;
  } else if (formatAll) {
    filesToFormat = null;
  } else {
    filesToFormat = getModifiedMarkdownFiles();

    if (!filesToFormat || filesToFormat.length === 0) {
      console.log('No modified markdown files to format.');
      return;
    }
  }

  try {
    if (filesToFormat) {
      const fileArgs = filesToFormat.map(f => `"${f}"`).join(' ');
      execSync(`npx --yes markdownlint-cli2 ${fileArgs} --fix`, {
        stdio: 'inherit'
      });
    } else {
      execSync('npx --yes markdownlint-cli2 "**/*.md" --fix', {
        stdio: 'inherit'
      });
    }
  } catch {
    // Continue into table formatting so one linter warning does not skip table cleanup.
  }

  const tableFormatterPath = join(__dirname, 'format-tables.cjs');
  const cmd = filesToFormat
    ? `node "${tableFormatterPath}" ${filesToFormat.map(f => `"${f}"`).join(' ')}`
    : `node "${tableFormatterPath}"`;

  execSync(cmd, {
    stdio: 'inherit'
  });
}

formatMarkdown();
