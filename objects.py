"""
# SQLObject SUUUUCKS
class Property_Unit( SQLObject, PegasusObject ):

	address = ForeignKey( 'Loc_Address', alternateID=True )
	property = ForeignKey( 'Property', default=None )
	leases = MultipleJoin( 'Property_Unit_Lease', joinColumn='unit_id' )
	price = FloatCol( default=0 )
	managers = MultipleJoin('Property_Access', joinColumn='unit_id')

	invoices = SQLRelatedJoin( 'Payment_Invoice', createRelatedTable=False )

class Property_Access(SQLObject):
	property = ForeignKey('Property', default=None)
	unit = ForeignKey('Property_Unit', default=None)
	manager = ForeignKey('Property_Manager', default=None)
	manager_type = ForeignKey('Property_Access_Type')
	receiver = BoolCol( default=False )
	status = EnumCol( enumValues=( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' )

class Property_Unit_Lease( SQLObject, PegasusObject ):
	unit = ForeignKey( 'Property_Unit' )
	recurring_invoice = ForeignKey( 'Payment_Invoice_Recurring', default=None, cascade='null', unique=True )
	members = MultipleJoin( 'Property_Unit_Lease_Member', joinColumn='lease_id', orderBy='defunct' )
	defunct_members = MultipleJoin( 'Property_Unit_Lease_Member', joinColumn='lease_defunct_id', orderBy='defunct' )
	defunct = BoolCol( default=False )

class Payment_Invoice( SQLObject, PegasusObject ):
	issued_date = DateTimeCol( default=sqlbuilder.func.NOW() )
	due_date    = DateCol( default=sqlbuilder.func.NOW() )
	receiver_due_date    = DateCol( default=sqlbuilder.func.NOW() )
	ship_date    = DateTimeCol( default=sqlbuilder.func.NOW() )
	individual_payers = BoolCol( default=None )
	payee       = ForeignKey( 'Payment_Account' )
	payee_status = EnumCol( enumValues=('pending','allowed','denied'), default='pending' )
	paid        = BoolCol( default=False )
	paid_date   = DateTimeCol( default=None )
	custom      = BoolCol( default=False )
	type = ForeignKey( 'Payment_Invoice_Type' )
	description = StringCol( default='' )
	note        = StringCol( default='' )
	parent_recurring_invoice = ForeignKey( 'Payment_Invoice_Recurring', default=None )
	payers      = MultipleJoin( 'Payment_Invoice_Payer', joinColumn='invoice_id' )
	items    = MultipleJoin( 'Payment_Invoice_Item', joinColumn='invoice_id' )
	item_amounts = MultipleJoin( 'Payment_Invoice_Item_Payer_Amount', joinColumn='invoice_id' )
	is_template = BoolCol( default=False )
	available_balance = FloatCol( default=0 )
	account_number = StringCol(length=256,default=None)
"""

# SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class Building(Base):
	__tablename__ = 'property'

	id = Column(Integer, primary_key=True)
	#address_id = Column(Integer, ForeignKey('loc__address.id'))


class Property_Access(Base):
	__tablename__ = 'property__access'

	id = Column(Integer, primary_key=True)
	property_id = Column(Integer, ForeignKey('property.id'))
	#unit_id = Column(Integer, ForeignKey('property__unit.id'))
	#manager = Column(Integer, ForeignKey('property__manager.id'))
	#manager_type = Column(Integer, ForeignKey('property__access__type.id'))
	receiver = Column(Integer, default=False )
	status = Column(Enum('unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked'), default='unknown')


_session = sessionmaker()
_engine = create_engine('sqlite:///_rentshare_test.db')
_session.configure(bind=_engine)

#_engine.dialect.has_table(_engine.connect(),
#                                         TABLE_NAME) == False:
Base.metadata.create_all(_engine)

if __name__ == '__main__':
	session = _session()

	building = Building()
	building_access = Property_Access( property_id=building.id )

	session.add(building )
	session.add(building_access)


	session.commit()
	print 'New Building (id: {})'.format(building.id)

print "poop"