# Coding Patterns GitBook

This repository contains documentation for common coding patterns organized as a GitBook.

> **Inspired by**: This content follows the structure from [Grokking the Coding Interview](https://www.designgurus.io/course/grokking-the-coding-interview) by DesignGurus.io, but provided as a free and open-source alternative! 🚀

## 📚 Documentation

View the live documentation: [GitHub Pages URL will be here after deployment]

## 🚀 Local Development

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/lvluu/leet.git
cd leet
```

2. Install GitBook CLI globally:
```bash
npm install -g gitbook-cli
```

3. Install dependencies:
```bash
gitbook install
```

4. Serve the book locally:
```bash
gitbook serve
```

The documentation will be available at `http://localhost:4000`

### Build

To build the static site:
```bash
gitbook build
```

The output will be in the `_book` directory.

## 📖 Structure

```
.
├── docs/
│   ├── README.md              # Introduction
│   ├── SUMMARY.md            # Table of Contents
│   ├── two-pointers/         # Two Pointers Pattern
│   │   ├── introduction.md
│   │   └── fast-slow.md
│   └── sliding-window/       # Sliding Window Pattern
│       ├── introduction.md
│       └── advanced-techniques.md
    ──── ... merge-intervals/       # Merge Intervals Pattern
        ├── introduction.md
        └── advanced-techniques.md
├── book.json                 # GitBook configuration
├── .gitbook.yaml            # GitBook root configuration
└── .github/
    └── workflows/
        └── gitbook.yml      # GitHub Actions workflow
```

## 🔄 Deployment

The documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch.

### Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" section
3. Set source to "gh-pages" branch
4. Save the changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This documentation is available for educational purposes.

## 🔗 Links

- [GitBook Documentation](https://docs.gitbook.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
