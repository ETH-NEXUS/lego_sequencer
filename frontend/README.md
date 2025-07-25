# Lego Sequencer Frontend

This is the Vue-based frontend for the Lego Sequencer project. It provides an interface to visualize and interact with the color stack reader and Google image results.

## ⚙️ Project Setup

### 0. Install Node.js and Yarn

If you don’t already have Node.js and Yarn installed:

#### On macOS with Homebrew:

```bash
brew install node@16
brew install yarn
brew link --overwrite --force node@16
```

#### Or install manually:

* [Node.js LTS Downloads](https://nodejs.org/en/download/releases/)
* [Yarn Installation Guide](https://classic.yarnpkg.com/en/docs/install)

### 1. Install dependencies

```bash
yarn install
```

> **Note:** This project may fail to build with Node.js v17+.
> Use Node.js **v16** for best compatibility.
> You can manage versions with [nvm](https://github.com/nvm-sh/nvm):
>
> ```bash
> nvm install 16
> nvm use 16
> ```
>
> **Alternative without nvm:**
> If you're not using `nvm`, consider installing [Node 16 LTS](https://nodejs.org/en/download/releases/) manually, and setting it as your system default.
> On macOS with Homebrew:
>
> ```bash
> brew install node@16
> brew link --overwrite --force node@16
> ```
>
> **Workaround for Node.js 17+**
> If you must use a newer Node version, you can bypass the OpenSSL error by setting:
>
> ```bash
> export NODE_OPTIONS=--openssl-legacy-provider
> yarn run serve
> ```
>
> This allows the dev server to run, but compatibility is not guaranteed.

---

## 📆 Production Build

### Compile and minify the frontend for deployment:

```bash
yarn run build
```

This creates a `dist/` folder you can serve via the sequencer backend.

## 🔧 Configuration

See [Vue CLI Configuration Reference](https://cli.vuejs.org/config/) for advanced options.

## 🛡️ Security Notes

This frontend is not exposed to the public web and does not process sensitive data.  
Security alerts (e.g., Dependabot warnings) are intentionally ignored for development convenience.