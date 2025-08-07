# Images Directory

This directory is for slideshow images on the homepage.

## How to Add Your Images

1. Add your images to this directory with descriptive names like:
   - `slide1.jpg`
   - `slide2.jpg`
   - `slide3.jpg`
   - etc.

2. Update the `index.html` file to reference your images:
   - Look for the `<div class="slideshow-container">` section
   - Replace the placeholder URLs with your image paths like: `images/slide1.jpg`

## Recommended Image Specifications

- **Size**: 600x400 pixels (or similar aspect ratio)
- **Format**: JPG, PNG, or WebP
- **File Size**: Keep under 500KB for fast loading
- **Content**: High-quality images related to learning, technology, or education

## Example Code to Update

Replace the current placeholder images in `index.html`:

```html
<div class="slide active">
    <img src="images/slide1.jpg" alt="Your Image Description">
</div>
<div class="slide">
    <img src="images/slide2.jpg" alt="Your Image Description">
</div>
```

The slideshow will automatically cycle through all images every 4 seconds!