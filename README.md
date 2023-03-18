# Fluffin Static Website Generator

Fluffin is a lightweight static website generator designed to help you quickly build and deploy static websites. With Fluffin, you can easily create and manage your website content, customize your design, and publish your site to the web.

## Features:

- opinionated design to be as simple as possible to jump in an operate
- should scale enough for small to medium static projects
- langage agnosic : You can generate HTML | XML | JSON ... whatever file you want in the end.
- simple but effective hot reload for html websites system
- minimal dependencies (python) that should let build final version from simple commands (cloud flare pages, netlify ...)

## Installation

To install Fluffin, simply run the following command:

```python
pip install fluffin
```

## Usage

Fluffin provides a range of commands to help you create and manage your static website. Here are some of the most commonly used commands:

`fluffin --help`
Displays the list of available commands and options.

`fluffin --dev`
Runs the development server, which allows you to preview your site locally before publishing it.

## Folder Structure & development process

Fluffin is designed to be KISS by having very few opiniated concepts described below:

run `fluffin --dev` to start build static content with a simple hot reload feature allowing convinient development process.

When you run Fluffin in your current folder, it will create a folder structure on-the-fly to help organize your website content. Here's a breakdown of the folders that Fluffin will create:

- `templates/pages/`: This folder contains the HTML templates for your website pages. Each file in this folder corresponds to a specific page on your website, and Fluffin will use these files to generate the final HTML output for your site.

- `templates/layout/`: This folder contains Jinja2 layout files that your pages can inherit from. These layout files define the overall structure of your website, including the header, footer, and any other common elements that appear on multiple pages.

- `templates/partials/`: This folder contains reusable HTML chunks, or "partials," that can be included in your templates. For example, you might create a partial for a navigation menu or a footer that appears on every page.

- `templates/static/`: This folder contains any static content (such as images, CSS files, or JavaScript files) that your website needs. Fluffin will copy these files into the appropriate location in the final output directory.

## Build

running fluffin command build just build `templates` content to dist folder acordingly.

I hope you find Fluffin helpful for building your static websites!
