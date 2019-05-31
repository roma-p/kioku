<h3>{{selector}} ({{number}})</h3>
<table>
<tr><th>name</th><th>items number</th></tr>
%for selector_id in selector_id_list:
    <tr>
    %for col in selector_id:
        <td>{{!col}}</td>
    %end
    </tr>
%end
</table>