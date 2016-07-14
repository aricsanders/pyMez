<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 04/2010 Style sheet that maps state xml sheets to html-->


<xsl:template match="/">
<html>   
<body>

<h2> Data Table: </h2>
<xsl:apply-templates/> 
<br/><br/>
<hr/>
</body>
</html>
</xsl:template>

<!-- Template for entries-->
<xsl:template match="/">
<h3>State</h3>

<xsl:for-each select="./*">
<table border='true'>
<tr><td><b><i><xsl:value-of select="name()"/></i></b></td>
<td><xsl:value-of select="."/></td> </tr>
</table>
</xsl:for-each>
</xsl:template>
<xsl:template match='/'>
       <h3>State Descripton</h3>
		<table border='2' bgcolor='white' cellpadding="1" bordercolor='black' bordercolorlight='black'>
		    
            <xsl:for-each select="//State_Description/*">
      
            
            <xsl:if test="name()!='Instrument_Description'">
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td><xsl:value-of select="."/></td></tr>
            </xsl:if>
            <xsl:if test="name()='Instrument_Description'">
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td><a><xsl:attribute name="href"> <xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a></td></tr>
            </xsl:if>           


		    </xsl:for-each>
           

		</table>
        <h3>State</h3>
		<table border='2' bgcolor='white' cellpadding="1" bordercolor='black' bordercolorlight='black'>
		    <tr>
            <xsl:for-each select="//State/Tuple[1]/@*">
            
            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>
            
            </xsl:for-each>
            </tr>
            <xsl:for-each select="//State/Tuple">
            <tr>
		    
            <xsl:for-each select="./@*">
         
                <td><xsl:value-of select="."/></td>
            
		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
    </xsl:template>
<xsl:template match='//Instrument_Description/*'>
<a><xsl:attribute name="href"> <xsl:value-of select="."/></xsl:attribute> HERE </a>
</xsl:template>
</xsl:stylesheet>
