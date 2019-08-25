<div class="header">
	<div class="center"><h1>{{!title}}</h1></div>
	<div class="center">
		%for selector_link in selector_link_list : 
			<tr>{{!selector_link}}</tr>
		%end
	</div>
	<div class="center"><form action="/search" method="GET">
	  <input type="text" size="80" maxlength="80" name="input">
	  <input type="submit" name="search" value="search">
	</form></div>
</div>