<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:asn="http://purl.org/ASN/schema/core/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="/" xml:space="preserve">
<InterchangeAssessmentMetadata xmlns="http://ed-fi.org/0100"><xsl:for-each select="//asn:Statement"><xsl:if test="asn:statementNotation">
    <Assessment>
        <AssessmentTitle><xsl:value-of select="asn:statementNotation"/></AssessmentTitle>
        <AssessmentIdentificationCode IdentificationSystem="Federal">
            <ID><xsl:value-of select="asn:statementNotation"/></ID>
        </AssessmentIdentificationCode>
        <AssessmentCategory>Portfolio assessment</AssessmentCategory>
        <AcademicSubject>Mathematics</AcademicSubject>
        <GradeLevelAssessed><xsl:choose xml:space="default">
            <xsl:when test="contains(substring(asn:statementNotation,19,1), 'K')">Kindergarten</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '1')">First grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '2')">Second grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '3')">Third grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '4')">Fourth grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '5')">Fifth grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '6')">Sixth grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '7')">Seventh grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), '8')">Eighth grade</xsl:when>
            <xsl:when test="contains(substring(asn:statementNotation,19,1), 'H')">Other</xsl:when>
            <xsl:otherwise>Ungraded</xsl:otherwise>
</xsl:choose></GradeLevelAssessed>
    </Assessment></xsl:if></xsl:for-each>
 </InterchangeAssessmentMetadata>
    </xsl:template>
</xsl:stylesheet>