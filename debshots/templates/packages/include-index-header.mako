# -*- coding: utf-8 -*-

<div class="graybox">
<h1>Browsing screenshots</h1>
${ h.tags.form(h.url_for())}
<p>
    By name
    |
    By category
    |
    Without screenshots
    ## Admin options:
    % if 'username' in session:
    |
    <a href="/packages/moderate">Moderation queue</a>
    % endif
    ## Search field
    |
    Search for: ${ h.tags.text(name='search') }
</p>
</form>
</div>
