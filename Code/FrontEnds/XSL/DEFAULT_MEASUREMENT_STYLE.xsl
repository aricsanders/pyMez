<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
<!--Written by Aric Sanders 04/2010 Style sheet that maps measurement xml sheets to html-->


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
<xsl:template match="Data_Description">
<h3> Data Description </h3>
<xsl:for-each select="./*">
<table border='true'>
<tr><td><b><i><xsl:value-of select="name()"/></i></b></td>
<td><xsl:value-of select="."/></td> </tr>
</table>
</xsl:for-each>
</xsl:template>
<xsl:template match='/'>
		<h3>Data Description:</h3>
		 <table>
            <xsl:for-each select="//Data_Description/*">
            <xsl:if test=".!='' and name()!='Instrument_Description'">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>

            <xsl:if test="name()='Instrument_Description'">
            <tr><th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th><td><a><xsl:attribute name="href"> <xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a></td></tr>
            </xsl:if> 
            </xsl:for-each>
         </table>
        <h3>Data:</h3>
		<table border='2' bgcolor='white' cellpadding="1" bordercolor='black' bordercolorlight='black'>
		    <tr>
            <xsl:for-each select="//Data/Tuple[1]/@*">
            
            <th bgcolor='silver'><b><xsl:value-of select="name()"/></b></th>
            
            </xsl:for-each>
            </tr>
            <xsl:for-each select="//Data/Tuple">
            <tr>
		    
            <xsl:for-each select="./@*">
         
                <td><xsl:value-of select="."/></td>
            
		    </xsl:for-each>
            </tr>
            </xsl:for-each>
		</table>
    </xsl:template>
</xsl:stylesheet>
