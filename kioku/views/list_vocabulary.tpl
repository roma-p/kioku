<div class='list_vocabulary'>
	<table>
	<tr>
	%for row in vocab_format: 
		<th>{{row}}</th>
	%end
	</tr>
	%for vocab in vocab_list:
	    <tr>
	    %for col in vocab:
	        <td>{{!col}}</td>
	    %end
	    </tr>
	%end
	</table>
</div>