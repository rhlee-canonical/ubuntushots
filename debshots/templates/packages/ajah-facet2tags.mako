# -*- coding: utf-8 -*-
<!-- Show tags of a debtags facet -->

% for tag in c.tags:
<div>
    ${ tag.description.splitlines()[0] }
</div>
% endfor
