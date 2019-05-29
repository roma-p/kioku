<h3>{{list_name}}</h3>
<table>
<tr><th>name</th><th>items number</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>
<tr>see all ({{number}})</tr>