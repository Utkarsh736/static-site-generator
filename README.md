# Static Site Generator

A powerful and elegant static site generator written in Python. It converts Markdown content into a fully static website using a flexible HTML template system. Built from scratch as part of the [Boot.dev](https://www.boot.dev/) "Build a Static Site Generator" course.

**Live Demo:** [https://utkarsh736.github.io/static-site-generator/](https://utkarsh736.github.io/static-site-generator/)

---

## Features

- ✨ **Full Markdown Support**
  - Headings (H1-H6)
  - Paragraphs with inline formatting (bold, italic, code)
  - Ordered and unordered lists
  - Blockquotes
  - Code blocks
  - Images and links
  
- 🎨 **Template System**
  - Consistent HTML templating across all pages
  - Dynamic title and content injection
  - Custom CSS styling
  
- 🔄 **Recursive Page Generation**
  - Automatically crawls nested content directories
  - Preserves directory structure in output
  - Supports unlimited nesting levels
  
- 🚀 **GitHub Pages Ready**
  - Configurable base path for deployment
  - Automatic URL rewriting for subdirectory hosting
  - Deploys directly from repository
  
- 📦 **Static Asset Management**
  - Automatic copying of images, CSS, and other assets
  - Maintains directory structure
  - Smart file handling

---

## Project Structure

```
static-site-generator/
├── src/
│   ├── main.py                 # Entry point and CLI
│   ├── textnode.py            # Text node representation
│   ├── htmlnode.py            # HTML node classes (HTMLNode, LeafNode, ParentNode)
│   ├── inline_markdown.py     # Inline markdown parsing (bold, italic, links, etc.)
│   ├── block_markdown.py      # Block-level parsing (headings, lists, quotes, etc.)
│   ├── test_*.py              # Unit tests
│
├── content/                   # Markdown source files
│   ├── index.md
│   ├── blog/
│   │   ├── glorfindel/
│   │   │   └── index.md
│   │   ├── tom/
│   │   │   └── index.md
│   │   └── majesty/
│   │       └── index.md
│   └── contact/
│       └── index.md
│
├── static/                    # Static assets (copied to output)
│   ├── index.css
│   └── images/
│       ├── tolkien.png
│       ├── glorfindel.png
│       ├── tom.png
│       └── rivendell.png
│
├── docs/                      # Generated site output (for GitHub Pages)
│   ├── index.html
│   ├── blog/
│   ├── contact/
│   ├── images/
│   └── index.css
│
├── template.html              # HTML template
├── main.sh                    # Local development script
├── build.sh                   # Production build script
├── test.sh                    # Run all tests
└── README.md
```

---

## Requirements

- **Python 3.10+**
- No external dependencies (only Python standard library modules are used)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Utkarsh736/static-site-generator.git
   cd static-site-generator
   ```

2. **Ensure content and static directories exist** (they are already included in this repo, but for new projects you can create them with):
   ```bash
   mkdir -p static/images content
   ```

---

## Usage

### Local Development

Run the generator with local paths:

```bash
./main.sh
```

This will:
1. Generate the site to `docs/` directory
2. Start a local web server at `http://localhost:8888`

Visit `http://localhost:8888` in your browser to view the site.

### Production Build (for GitHub Pages)

Build with the correct base path for your GitHub Pages URL:

```bash
./build.sh
```

**Note:** Update `build.sh` with your repository name:
```bash
python3 src/main.py "/your-repo-name/"
```

### Running Tests

Run the complete test suite:

```bash
./test.sh
```

---

## How It Works

### Architecture

The static site generator follows a multi-stage pipeline:

```
Markdown Files
    ↓
markdown_to_blocks() → Split into block-level elements
    ↓
block_to_block_type() → Classify blocks (heading, list, quote, etc.)
    ↓
Block-specific converters → Convert to HTMLNode objects
    ↓
text_to_textnodes() → Parse inline markdown (bold, italic, links)
    ↓
text_node_to_html_node() → Convert to LeafNode objects
    ↓
HTMLNode.to_html() → Render final HTML string
    ↓
Template injection → Inject into HTML template
    ↓
Final HTML Pages
```

### Core Components

1. **TextNode** - Represents inline text with a type (text, bold, italic, code, link, image)
2. **HTMLNode** - Base class for HTML representation
3. **LeafNode** - HTML nodes with no children (e.g., `<b>`, `<a>`, `<img>`)
4. **ParentNode** - HTML nodes with children (e.g., `<div>`, `<p>`, `<ul>`)
5. **Block Parsers** - Convert markdown blocks to HTML
6. **Inline Parsers** - Handle inline formatting within blocks

---

## Customization

### Adding New Pages

Create a new Markdown file in the `content/` directory:

```bash
echo "# My New Page" > content/new-page.md
```

Run the generator and the page will be created at `docs/new-page.html`.

### Changing Styles

Edit `static/index.css` to customize the appearance:

```css
body {
  background-color: #1f1c25;
  color: #f0e6d1;
  font-family: "Luminari", "Georgia", serif;
}
```

### Modifying the Template

Edit `template.html` to change the page structure:

```html
<!doctype html>
<html>
  <head>
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

### Adding Static Assets

Place images, fonts, or other assets in `static/`:

```bash
cp my-image.png static/images/
```

They'll be automatically copied to `docs/images/` on the next build.

---

## Deployment (GitHub Pages)

1. **Build the site:**
   ```bash
   ./build.sh
   ```

2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Deploy site"
   git push origin main
   ```

3. **Configure GitHub Pages:**
   - Go to repository **Settings** → **Pages**
   - Set source to `main` branch and `/docs` folder
   - Save and wait for deployment

4. **Visit your site:**
   ```
   https://USERNAME.github.io/REPO_NAME/
   ```

---

## Testing

The project includes comprehensive unit tests:

- `test_textnode.py` - TextNode and conversion tests
- `test_htmlnode.py` - HTMLNode hierarchy tests
- `test_leafnode.py` - LeafNode rendering tests
- `test_parentnode.py` - ParentNode recursive tests
- `test_inline_markdown.py` - Inline parsing tests
- `test_block_markdown.py` - Block parsing and HTML generation tests

Run all tests:
```bash
./test.sh
```

---

## What I Learned

Building this project taught me:

- **Recursive algorithms** for parsing nested structures
- **Object-oriented design** with clean class hierarchies
- **Regular expressions** for pattern matching in markdown
- **Test-driven development** with comprehensive unit tests
- **File I/O operations** and directory traversal
- **Template systems** and string manipulation
- **Deployment workflows** with GitHub Pages

---

## Acknowledgements

- Built as part of the [Boot.dev](https://www.boot.dev/) "Build a Static Site Generator" course
- Inspired by static site generators like Jekyll, Hugo, and Eleventy
- Themed around J.R.R. Tolkien's legendarium

---

## License

This project is licensed under the MIT License.

---

## Author

**Utkarsh Singh**
- GitHub: [@Utkarsh736](https://github.com/Utkarsh736)
- Project Link: [https://github.com/Utkarsh736/static-site-generator](https://github.com/Utkarsh736/static-site-generator)

---

## Future Enhancements

Potential improvements for the future:

- [ ] Add syntax highlighting for code blocks
- [ ] Support for custom front matter (metadata)
- [ ] RSS feed generation for blog posts
- [ ] Sitemap generation
- [ ] Table of contents auto-generation
- [ ] Tag and category support
- [ ] Search functionality
- [ ] Hot reload during development
- [ ] Markdown table support
- [ ] Multiple template support

---

*"Not all those who wander are lost." - J.R.R. Tolkien*
