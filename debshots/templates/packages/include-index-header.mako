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
    <a href="/packages">All packages</a>
    |
    <a href="/packages/with_screenshots">Packages with screenshots</a>
    |
    <a href="/packages/without_screenshots">Packages missing any screenshots</a>
    ## Admin options:
    % if 'username' in session:
    |
    <a href="/packages/moderate">Moderation queue</a>
    % endif
</p>
<p>
    ## Search field
    Search term: ${ h.tags.text(name='search', value=request.params.get('search')) }
    % if c.debtags_search:
    | List debtag: ${ c.debtags_search }
    % endif
</p>
<div>
    <input type="submit" value="Show" />
</div>
</form>
</div>
