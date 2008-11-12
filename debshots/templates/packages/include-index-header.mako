# -*- coding: utf-8 -*-

<script type="application/x-javascript">
    $(document).ready(function() {
        $('input[name=search]').focus();
    });
</script>


<div class="graybox">
<h1>Browsing screenshots</h1>
${ h.tags.form(h.url_for())}
<p>
    <a href="/packages">All packages</a>
    |
    <a href="/packages/without_screenshots">Without screenshots</a>
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
