<h2>{{word}}</h2>
<h4>{{prononciation}}</h4>
<div>{{meaning}}</div>
<div>  </div>
<div>example: {{example}}</div>
<div>categorie: {{!categorie}}</div>
<div>tag: {{!tag}}</div>
<div>kanjis: 
	<table>
	%for kanji in kanjis:
	    <tr>{{!kanji}}, </tr>
	%end
	</table>
</div>
