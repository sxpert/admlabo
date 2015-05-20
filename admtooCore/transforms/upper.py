from django.db.models import Transform

class UpperCase(Transform) :
	lookup_name = 'upper'
	bilateral = True

	def as_sql (self, compiler, connection) :
		lhs, param = compiler.compile (self.lhs)
		return "UPPER(%s)" % lhs, param

from django.db.models import CharField, TextField
CharField.register_lookup(UpperCase)
import sys
sys.stderr.write ('registered for CharField\n')
sys.stderr.flush ()
TextField.register_lookup(UpperCase)
