<table>
<tr><th>word</th><th>prononciation</th><th>meaning</th><th>
%for vocab in vocab_list:
    <tr>
    %for col in vocab:
        <td>{{!col}}</td>
    %end
    </tr>
%end
</table>