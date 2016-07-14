<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 10/2009 Style sheet that maps Instrument xml sheets to html-->


<xsl:template match="/">
<html>   
<body>
<!-- Print a Description if it exists-->
<h2> Description: </h2>
<h3><xsl:value-of select="//Entry[@Id='-1']"/></h3>
<a href="#last_section"> Go to the last </a>
<xsl:apply-templates/> 

<br/><br/>
<hr/>
<a name="last_section"><h2> End of the Page</h2></a>
</body>
</html>
</xsl:template>

<!-- Template for entries-->
<xsl:template match="Entry">
<xsl:for-each select=".">
<xsl:if test="@Id !=-1">
<br/>
<hr/>
<b><i> Entry: </i></b><xsl:value-of select="./@Id"/><br/> 
<b><i><a><xsl:attribute name="href"> about_date;<xsl:value-of select="./@Id"/>;<xsl:value-of select="./@Date"/></xsl:attribute> Date: </a></i></b> 
<xsl:value-of select="./@Date"/><br/>
<b><a><xsl:attribute name="href"> edit_value;<xsl:value-of select="./@Id"/>;<xsl:value-of select="./@Date"/></xsl:attribute> Edit</a></b>
<br/><xsl:value-of select="."/>
</xsl:if> 
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>