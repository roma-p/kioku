<h3>{{result_type}} : {{!result_value}}</h3>
<tr>
%if examples_list : 
	%for row in examples_list: 
		<th>{{!row}}, </th>
	%end
%end
</tr>