<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 01/2011 Style sheet that maps log xml sheets to html-->


<xsl:template match="/">
<html>   
<body>
<!-- Print a Description if it exists-->
<h2> Description: </h2>
<h3><xsl:value-of select="//Entry[@Id='-1']"/></h3>
<xsl:apply-templates/> 
<br/><br/>
<hr/>
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
<b><i> Date: </i></b> <xsl:value-of select="./@Date"/><br/>





    <br/>
    <xsl:for-each select=".">
    <b> Actions:</b> <xsl:value-of select="Actions"/><br/>   
    <b> Taken By:</b> <xsl:value-of select="Who_Did"/><br/>
    <b> Suggested By:</b><xsl:value-of select="Who_Suggested"/><br/>
    <b>Conclusion:</b><xsl:value-of select="Conclusion"/><br/>
    <b>New Data Location:</b> <xsl:value-of select="Data_Location"/><br/>
    <b>New Data's URL :</b>
    <ol>
    <xsl:for-each select="URL">
    <li><a><xsl:attribute name="href"> <xsl:value-of select="." /> </xsl:attribute>  <xsl:value-of select="."/></a></li>
    </xsl:for-each>
    </ol>

    </xsl:for-each>   
            
    
</xsl:if> 
</xsl:for-each>

</xsl:template>
</xsl:stylesheet>
