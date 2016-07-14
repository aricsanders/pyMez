<?xml version="1.0" encoding="ISO-8859-1"?>
<!--Written by Aric Sanders 04/2008-->

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:h="http://www.w3.org/1999/xhtml">
<!-- I am still supiscious that the way namespaces work in these browsers is not right, but they should be in the root tag (like the html tag)-->
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'/>
	<xsl:template match="/">
		<html>
		<head>
		<title><xsl:value-of select="//Name"/></title>
		</head>
		<body>
  
		<h2>Instrument: <xsl:value-of select="//Name"/></h2>
        <i>Made By: <a><xsl:attribute name="href"> <xsl:value-of select="//Manufacturer_Website/@href"/></xsl:attribute> <xsl:value-of select="//Manufacturer"/></a></i><br/>
		
        <xsl:apply-templates/>

		    
		</body>
		</html>
	</xsl:template>

    <xsl:template match='Specific_Information'>
    <img><xsl:attribute name="src"> <xsl:value-of select="//Image/@href"/> </xsl:attribute> </img>
		<a><xsl:attribute name="href"> <xsl:value-of select="//Manual/@href"/></xsl:attribute> <h3>Manual </h3></a>
		 <table>
            <xsl:for-each select="./*">
            <xsl:if test=".!=''">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>
            </xsl:for-each>
         </table>
		<hr/>	<br/>
    </xsl:template>

    <xsl:template match='General_Information'>
    <xsl:apply-templates select='Commands'/>
    </xsl:template>

    <xsl:template match='Commands'>
		<h3>Commands:</h3>
		 <table>
            <xsl:for-each select="//Commands_Description/*">
            <xsl:if test=".!=''">
            <tr><td><b><xsl:value-of select="name()"/> :</b> </td><td><xsl:value-of select="."/></td></tr>
            </xsl:if>
            </xsl:for-each>
         </table>
    
		<table border='2' bgcolor='silver' cellpadding="4" bordercolor='black' bordercolorlight='black'>
		    <tr>
            <th><big>Command</big></th>
            <th><big>Type</big></th>
            <th><big>Argument</big></th>
            <th><big>Returns</big></th>
            <th><big>Description</big></th>
            </tr>
            <xsl:for-each select="//Commands/Tuple">
		    <tr>
                <td><b><xsl:value-of select="./@Command"/></b></td>
                <td style='color:red'><xsl:value-of select="./@Type"/></td>
                <td style='color:blue'><xsl:value-of select="./@Argument"/></td>
                <td style='color:blue'><xsl:value-of select="./@Returns"/></td>
                <td><i><xsl:value-of select="./@Description"/></i></td>

            </tr>
		    </xsl:for-each>

		</table>
        <h3> State Commands </h3>
        <table border='2' bgcolor='silver' cellpadding="4" bordercolor='black' bordercolorlight='black'>
		    <tr>
            <th><big>Command to Set state</big></th>
            <th><big>Command to Query state</big></th>
            </tr>
            <xsl:for-each select="//State_Commands/Tuple">
		    <tr>
                <td><b><xsl:value-of select="./@Set"/></b></td>
                <td><b><xsl:value-of select="./@Query"/></b></td>
               
            </tr>
            </xsl:for-each>
        </table>
        
    </xsl:template>

</xsl:stylesheet>