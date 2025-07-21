import { promises as fs } from 'fs';
import path from 'path';
import chalk from 'chalk';
import inquirer from 'inquirer';
import ora from 'ora';

export async function init(projectName?: string, options?: any) {
  console.log(chalk.cyan('\n🚀 Welcome to CRAITE!\n'));

  // Get project details
  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'name',
      message: 'Project name:',
      default: projectName || 'my-craite-project',
      validate: (input) => {
        if (/^[a-zA-Z0-9-_]+$/.test(input)) return true;
        return 'Project name can only contain letters, numbers, hyphens, and underscores';
      }
    },
    {
      type: 'list',
      name: 'template',
      message: 'Choose a template:',
      choices: [
        { name: 'Basic Web3 Project', value: 'basic' },
        { name: 'DeFi Protocol', value: 'defi' },
        { name: 'NFT Marketplace', value: 'nft' },
        { name: 'DAO Governance', value: 'dao' }
      ],
      default: options?.template || 'basic'
    }
  ]);

  const spinner = ora('Creating project...').start();

  try {
    // Create project directory
    const projectPath = path.join(process.cwd(), answers.name);
    await fs.mkdir(projectPath, { recursive: true });

    spinner.succeed(chalk.green('Project created successfully!'));

    console.log('\n' + chalk.cyan('Next steps:'));
    console.log(chalk.white(`  cd ${answers.name}`));
    console.log(chalk.white('  npm install'));
    console.log(chalk.white('  craite generate "Create an ERC20 token"'));
    
  } catch (error: any) {
    spinner.fail(chalk.red('Failed to create project'));
    throw error;
  }
}
