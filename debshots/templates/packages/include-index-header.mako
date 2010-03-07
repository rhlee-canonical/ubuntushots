# -*- coding: utf-8 -*-

<script type="application/x-javascript">
    $(document).ready(function() {
        $('input[name=search]').focus();
    });
</script>


<div class="graybox">
<h1>Browsing screenshots</h1>
${ h.tags.form(h.url.current())}
<p>
    <a href="/packages">Packages with screenshots</a>
    |
    <a href="/packages/without_screenshots">Packages missing any screenshots</a>
    ## Admin options:
    % if 'username' in session:
    |
    <a href="/packages/moderate">Moderation queue</a>
    % endif
    ## Search field
    |
    Search for: ${ h.tags.text(name='search', value=request.params.get('search')) }
</p>
</form>
</div>
