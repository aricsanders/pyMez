<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 10/2009 Style sheet that maps Instrument xml sheets to html-->


<xsl:template match="/">
<html>   
<body>
<!-- Print a Description if it exists-->
<h2> Description: </h2>
<h3><xsl:value-of select="//Entry[@Index='-1']"/></h3>
<xsl:apply-templates/> 
<br/><br/>
<hr/>
</body>
</html>
</xsl:template>

<!-- Template for entries-->
<xsl:template match="Entry">
<xsl:for-each select=".">
<xsl:if test="@Index !=-1">
<br/>
<hr/>
<b><i> Entry: </i></b><xsl:value-of select="./@Index"/><br/> 
<b><i> Date: </i></b> <xsl:value-of select="./@Date"/><br/>
<xsl:value-of select="."/>
</xsl:if> 
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>