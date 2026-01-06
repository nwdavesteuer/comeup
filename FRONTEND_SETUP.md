# Frontend Setup - Installing Node.js and npm

## The Error
You're seeing `zsh: command not found: npm` because Node.js (which includes npm) is not installed on your system.

## Solution: Install Node.js

### Option 1: Using Homebrew (Recommended for macOS)

1. **Install Homebrew** (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Node.js**:
   ```bash
   brew install node
   ```

3. **Verify installation**:
   ```bash
   node --version
   npm --version
   ```

### Option 2: Download from Official Website

1. Go to https://nodejs.org/
2. Download the LTS (Long Term Support) version for macOS
3. Run the installer
4. Restart your terminal
5. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Option 3: Using nvm (Node Version Manager) - Advanced

If you want to manage multiple Node.js versions:

1. **Install nvm**:
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   ```

2. **Restart terminal or run**:
   ```bash
   source ~/.zshrc
   ```

3. **Install Node.js**:
   ```bash
   nvm install --lts
   nvm use --lts
   ```

## After Installation

Once Node.js is installed, continue with the frontend setup:

```bash
cd /Users/jonahsteuer/Documents/GitHub/comeup/frontend
npm install
npm run dev
```

## Quick Check

Run these commands to verify everything is working:

```bash
node --version   # Should show something like v20.x.x
npm --version    # Should show something like 10.x.x
```

If both commands work, you're ready to proceed with the frontend setup!

