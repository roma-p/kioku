<h3>categorie : {{name or 'Not Found'}}</h3>
<table>
<tr><th>word</th><th>prononciation</th><th>meaning</th><th>example</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>