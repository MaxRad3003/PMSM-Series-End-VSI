with open('package_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'Keyboard navigation and Fullscreen (<kbd>F</kbd>) enabled',
    'Keyboard navigation and Fullscreen mode with <kbd>F</kbd> key'
)
text = text.replace(
    '<ul class="feature-list">',
    '<ul class="feature-list" dir="ltr" style="text-align: left;">',
    1 # only for the second card or we check card 2 specifically
)

with open('package_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated package_presentation.py")
