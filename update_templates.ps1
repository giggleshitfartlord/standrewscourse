for ($i = 3; $i -le 18; $i++) {
    $file = "templates/holes/hole_$i.html"
    $content = Get-Content $file -Raw
    
    # Get the hole name from the title block
    $titleMatch = [regex]::Match($content, 'block title %}Hole \d+ - (.*?) -')
    $holeName = $titleMatch.Groups[1].Value
    
    # Create the new layout
    $newLayout = @"
{% extends "base.html" %}

{% block title %}Hole $i - $holeName - Old Course Caddie{% endblock %}

{% block content %}
<div class="hole-card">
    <h1>Hole $i - "$holeName"</h1>
    
    <div class="row">
        <div class="col-md-5">
            <div class="hole-map-container">
                <img src="{{ url_for('static', filename='images/hole$i.webp') }}" alt="Hole $i Map" class="hole-map img-fluid">
            </div>
        </div>
        <div class="col-md-7">
"@

    # Get the content section (everything between first strategy-section and the last div)
    $contentMatch = [regex]::Match($content, '(?s)<div class="strategy-section">(.*)</div>\s*</div>\s*{% endblock %}')
    $contentSection = $contentMatch.Groups[1].Value

    # Create the complete new content
    $newContent = $newLayout + $contentSection + "</div></div></div>{% endblock %}"
    
    # Save the file
    $newContent | Out-File $file -Encoding UTF8
}
