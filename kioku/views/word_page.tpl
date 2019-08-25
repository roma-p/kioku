<div class="word_page">
	<div class="word_page_word_section">
		<div class="word_page_word">{{word}}</div>
		<div class="word_page_prononciation">{{prononciation}}</div>
		<div class="word_page_meaning">{{meaning}}</div>
	</div>

	%if example : 
		<div class="word_page_example">example:<br/>{{example}}</div>
	%end

	<div>categorie: {{!categorie}}</div>
	<div>tag: {{!tag}}</div>
	<div>kanjis: 
		<table>
		%for kanji in kanjis:
		    <tr>{{!kanji}}, </tr>
		%end
		</table>
	</div>
</div>