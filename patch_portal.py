with open('package_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<!-- Card 2: Interactive English Presentation -->\n        <div class="portal-card">',
    '<!-- Card 2: Interactive English Presentation -->\n        <div class="portal-card" dir="ltr" style="text-align: left;">'
)
text = text.replace(
    '<span class="card-icon">🇮🇱</span>',
    '<span class="card-icon">&#x1F4CA;</span>'
)
text = text.replace(
    '<span class="card-icon">🌐</span>',
    '<span class="card-icon">&#x1F310;</span>'
)

with open('package_presentation.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated package_presentation.py")
