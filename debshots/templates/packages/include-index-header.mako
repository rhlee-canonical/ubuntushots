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
    <a href="/packages">Package list</a>
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
