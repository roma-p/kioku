<div align="center">{{!title}}</div>
<div align="center">
	%for selector_link in selector_link_list : 
		<tr>{{!selector_link}}</tr>
	%end
</div>
<div align="center"><form action="/search" method="GET">
  <input type="text" size="100" maxlength="100" name="input">
  <input type="submit" name="search" value="search">
</form></div>