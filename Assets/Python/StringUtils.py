import re

def unicodeToXML(u):
	u = u.encode("ascii", "xmlcharrefreplace")
	return u

def unescape(s): #backported from python 2.7, see https://hg.python.org/cpython/file/2.7/Lib/HTMLParser.py#l447 vs https://hg.python.org/cpython/file/2.5/Lib/HTMLParser.py#l361
	if '&' not in s:
		return s
	def replaceEntities(s):
		s = s.groups()[0]
		try:
			if s[0] == "#":
				s = s[1:]
			if s[0] in ['x','X']:
				c = int(s[1:], 16)
			else:
				c = int(s)
				return unichr(c)

		except ValueError:
			return '&#'+s+';'

		else:
			# Cannot use name2codepoint directly, because HTMLParser supports apos,
			# which is not part of HTML 4
			import htmlentitydefs
			if RFGWB.entitydefs is None:
				entitydefs = RFGWB.entitydefs = {'apos':u"'"}
				for k, v in htmlentitydefs.name2codepoint.iteritems():
					entitydefs[k] = unichr(v)

			try:
				return entitydefs[s]

			except KeyError:
				return '&'+s+';'
	return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", replaceEntities, s)
