#!/usr/bin/env node

import { Command } from 'commander';
import { CRAITECore } from '@craite/core';
import chalk from 'chalk';
import ora from 'ora';
import * as fs from 'fs/promises';
import * as path from 'path';

const program = new Command();

program
  .name('craite')
  .description('CRAITE - Elite Web3 Code Generator & AI Development Platform')
  .version('1.0.1');

program
  .command('generate <type>')
  .description('Generate Web3 code')
  .option('-l, --language <language>', 'Programming language', 'solidity')
  .option('-o, --output <file>', 'Output file path')
  .action(async (type, options) => {
    const spinner = ora('Generating code...').start();
    
    try {
      // For now, use OpenAI directly
      const apiKey = process.env.OPENAI_API_KEY || process.env.CRAITE_API_KEY;
      if (!apiKey) {
        spinner.fail('API key not found. Set OPENAI_API_KEY or CRAITE_API_KEY');
        process.exit(1);
      }
      
      // This would use the actual core package
      spinner.succeed('Code generated successfully!');
      
      if (options.output) {
        await fs.writeFile(options.output, '// Generated code here');
        console.log(chalk.green(`✅ Saved to ${options.output}`));
      }
    } catch (error) {
      spinner.fail('Generation failed');
      console.error(error);
    }
  });

program.parse();
