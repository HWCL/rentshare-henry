"""
# SQLObject SUUUUCKS
class Property_Unit( SQLObject, PegasusObject ):

	address = ForeignKey( 'Loc_Address', alternateID=True )
	property = ForeignKey( 'Property', default=None )
	leases = MultipleJoin( 'Property_Unit_Lease', joinColumn='unit_id' )
	price = FloatCol( default=0 )
	managers = MultipleJoin( 'Property_Access', joinColumn='unit_id' )

	invoices = SQLRelatedJoin( 'Payment_Invoice', createRelatedTable=False )

class Property_Access( SQLObject ):
	property = ForeignKey( 'Property', default=None )
	unit = ForeignKey( 'Property_Unit', default=None )
	manager = ForeignKey( 'Property_Manager', default=None )
	manager_type = ForeignKey( 'Property_Access_Type' )
	receiver = BoolCol( default=False )
	status = EnumCol( enumValues=( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' )

class Property_Unit_Lease( SQLObject, PegasusObject ):
	unit = ForeignKey( 'Property_Unit' )
	recurring_invoice = ForeignKey( 'Payment_Invoice_Recurring', default=None, cascade='null', unique=True )
	members = MultipleJoin( 'Property_Unit_Lease_Member', joinColumn='lease_id', orderBy='defunct' )
	defunct_members = MultipleJoin( 'Propertyroperty_Unit_Lease_Member', joinColumn='lease_defunct_id', orderBy='defunct' )
	defunct = BoolCol( default=False )

class Payment_Invoice( SQLObject, PegasusObject ):
	issued_date = DateTimeCol( default=sqlbuilder.func.NOW() )
	due_date    = DateCol( default=sqlbuilder.func.NOW() )
	receiver_due_date    = DateCol( default=sqlbuilder.func.NOW() )
	ship_date    = DateTimeCol( default=sqlbuilder.func.NOW() )
	individual_payers = BoolCol( default=None )
	payee       = ForeignKey( 'Payment_Account' )
	payee_status = EnumCol( enumValues=( 'pending','allowed','denied' ), default='pending' )
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
	account_number = StringCol( length=256,default=None )

class Payment_Invoice_Recurring( SQLObject ):
	invoice_template = ForeignKey( 'Payment_Invoice' )
	cycle_offset= IntCol( default=1 )
	#cycle_freq  = IntCol( default=1 )
	due_offset= IntCol( default=0 )
	service_start_date = DateCol( default=None )
	service_end_date   = DateCol( default=None )
	prepay      = BoolCol( default=False )
	creation_date = DateTimeCol( default=sqlbuilder.func.NOW() )
	autopayers  = MultipleJoin( 'Payment_Invoice_Recurring_Autopayer', joinColumn='recurring_invoice_id' )
	invoices = SQLMultipleJoin( 'Payment_Invoice', joinColumn='parent_recurring_invoice_id', orderBy='-receiver_due_date' )
	defunct = BoolCol( default=False )
	defunct_date = DateTimeCol( default=None )

class Payment_Invoice_Payer( SQLObject, PegasusObject ):
	account = ForeignKey( 'Payment_Account' )
	invoice = ForeignKey( 'Payment_Invoice' )
	amount_paid = FloatCol( default=0 )
	paid = BoolCol( default=False )
	paid_date = DateTimeCol( default=None )
	admin = BoolCol( default=False )
	payments_transfered = BoolCol( default=False )
	payments_transfered_date = DateTimeCol( default=None )
	payments_transferable_by = DateTimeCol( default=None )
	defunct = BoolCol( default=False )
	item_amounts = MultipleJoin( 'Payment_Invoice_Item_Payer_Amount', joinColumn='payer_id' )

class Property_Manager( SQLObject, PegasusObject ):
	account = ForeignKey( 'Payment_Account' )
	master_manager = BoolCol( default=False )
	status = EnumCol( enumValues=( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' )
	num_units = IntCol( default=None )
"""

# SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
import datetime

Base = declarative_base()

class Unit( Base ):
	__tablename__ = 'property__unit'

	id 				= Column( Integer, primary_key=True )

	#address_id 	= Column( Integer, ForeignKey( 'loc__address.id' ) )

	property_id 	= Column( Integer, ForeignKey( 'property.id' ) )
	building   		= relationship( 'Building' )

	#leases 		= relationship( 'Lease' )
	price 			= Column( Float, default=0 )

	manager_access 	= relationship( 'Property_Access' )
	invoices 		= relationship( 'Invoice' )
	building   		= relationship( 'Building' )
	#address   		= relationship( 'Address' )

	"""
	#trying stuff out
	testclass1 			= relationship( 'Test_Class', primaryjoin='Unit.id==Test_Class.unit1_id', backref='Test_Class.unit1_id')
	testclass2 			= relationship( 'Test_Class', primaryjoin='Unit.id==Test_Class.unit2_id', backref='Test_Class.unit2_id')


class Test_Class( Base ):
	__tablename__ = 'test_table'

	id = Column( Integer, primary_key=True)
	unit1_id = Column( Integer, ForeignKey('property__unit.id') )
	unit2_id = Column( Integer, ForeignKey('property__unit.id') )

	"""


class Property_Access( Base ):
	__tablename__ = 'property__access'

	id 					= Column( Integer, primary_key=True )

	property_id 		= Column( Integer, ForeignKey( 'property.id' ) )
	building   			= relationship( 'Building' )

	unit_id 			= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 				= relationship( 'Unit' )

	manager_id 		= Column( Integer, ForeignKey( 'property__manager.id' ) )
	manager 			= relationship( 'Manager' )

	#manager_type_id 	= Column( Integer, ForeignKey( 'property__access__type.id' ) )
	#manager_type 		= relationship( 'Manager_Type' )

	receiver 			= Column( Integer, default=False )
	status 				= Column( Enum( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' )


class Lease( Base ):
	__tablename__ = 'property__unit__lease'

	id 						= Column( Integer, primary_key=True )

	unit_id 				= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 					= relationship( 'Unit' )

	#recurring_invoice_id 	= Column( Integer, ForeignKey( 'payment__invoice__recurring' ) )
	#recurring_invoice 		= relationship( 'Recurring_Invoice' )

	#members 				= relationship( 'Tenant', primaryjoin='Lease.id==Tenant.lease_id' )
	#defunct_members			= relationship( 'Tenant', primaryjoin='Lease.id==Tenant.lease_defunct_id' )

	defunct 				= Column( Boolean, default=False )

class Building( Base ):
	__tablename__ = 'property'

	id 			= Column( Integer, primary_key=True )
	#address_id = Column( Integer, ForeignKey( 'loc__address.id' ) )

class Invoice( Base ):
	__tablename__ = 'payment__invoice'

	id 							= Column( Integer, primary_key=True )

	#type_id 					= Column( Integer, ForeignKey( 'payment__invoice__type.id' ) )
	#payment_type 				= relationship( 'Payment_Type' )

	#payee_id 					= Column( Integer, ForeignKey( 'payment__account.id' ) )
	#payee 						= relationship( 'Payment_Account' )
	payee_status 				= Column( Enum( 'pending', 'allowed', 'denied' ), default='pending' )

	unit_id						= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 						= relationship( 'Unit' )

	#parent_recurring_invoice_id = Column( Integer, ForeignKey( 'payment__invoice__recurring.id' ), defualt=None )
	#recurring_invoice 			= relationship( 'Recurring_Invoice' )

	issued_date 				= Column( DateTime, default=func.current_timestamp() )
	due_date 					= Column( Date, default=func.current_timestamp() )
	receiver_due_date 			= Column( Date, default=func.current_timestamp() )
	ship_date 					= Column( DateTime, default=func.current_timestamp() )

	individual_payers 			= Column( Boolean, default=None )
	paid 						= Column( Boolean, default=False )
	paid_date 					= Column( DateTime, default=None )
	custom 						= Column( Boolean, default = False )
	description 				= Column( String, default='' )
	note 						= Column( String, default='' )
	#payers 					= relationship( 'payment__invoice__payer' )
	#items 						= relationship( 'payment__invoice__item' )
	#item_amounts 				= relationship( 'payment__invoice__item__payer__amount' )
	is_template 				= Column( Boolean, default=False )
	available_balance 			= Column( Float, default=0 )
	account_number 				= Column( String( length=256 ), default=None )


class Recurring_Invoice( Base ):
	__tablename__ = 'payment__invoice__recurring'

	id 					= Column( Integer, primary_key=True )

	invoice_template_id = Column( Integer, ForeignKey( 'payment__invoice.id' ) )
	invoice_template 	= relationship( 'Invoice' )

	cycle_offset 		= Column( Integer, default=1 )
	#cycle_freq			= Column( Integer, default=1 )
	due_offset			= Column( Integer, default=0 )

	service_start_date 	= Column( Date )
	service_end_date	= Column( Date )
	creation_date 		= Column( Date, default=func.current_timestamp() )


	prepay 				= Column( Boolean, default=False )
	#autopayers			= relationship( 'Payment_Invoice_Recurring_Autopayer' )
	invoices			= relationship( 'Invoice' )
	defunct 			= Column( Boolean, default=False )
	defunct_date		= Column( Date )


class Invoice_Payer( Base ):
	__tablename__ = 'payment__invoice__payer'

	id 							= Column( Integer, primary_key=True )

	#account_id 					= Column( Integer, ForeignKey( 'payment__account.id' ) )
	#account 					= relationship( 'Payment_Account' )

	amount_paid 				= Column( Float, default=0 )
	paid 						= Column( Boolean, default=False )
	paid_date 					= Column( DateTime )

	admin 						= Column( Boolean, default=False )
	payments_trasnfered 		= Column( Boolean, default=False )
	payments_transfered_date 	= Column( DateTime )
	payments_transferable_by 	= Column( DateTime )

	defunct 					= Column( Boolean, default=False )
	#item_amounts 				= relationship( 'Payment_Invoice_Item_Payer_Amount' )


class Property_Manager( Base ):
	__tablename__ = 'property__manager'

	id 				= Column( Integer, primary_key=True )

	#account_id 	= Column( Integer, ForeignKey( 'payment__account.id' ) )
	#account 		= relationship( 'Payment_Account' )

	master_manager 	= Column( Boolean, default=False )
	status 			= Column( Enum( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknnown' ) 

	num_units 		= Column( Integer )


_session = sessionmaker()
_engine = create_engine( 'sqlite:///_rentshare_test.db' )
_session.configure( bind=_engine )

#_engine.dialect.has_table( _engine.connect(),
#                                         TABLE_NAME ) == False:
Base.metadata.create_all( _engine )

if __name__ == '__main__':
	session = _session()

	#make some dummy properties


	qry = session.query(Unit, Property_Access, Property_Manager).filter(Property_Access.status=='unknown').orderBy(Property_Manager.status)

	"""
	building = Building()
	building_access = Property_Access( building=building )
	#access = Property_Access(  )
	#building.managers.append( access )

	session.add( building )
	session.add( building_access )


	session.commit()

	tc1 = Test_Class()
	tc2 = Test_Class()

	u1 = Unit( testclass1=[tc1], testclass2=[tc2] )
	u2 = Unit( testclass1=[tc2], testclass2=[tc1] )

	session.add( u1 )
	session.add( u2 )

	session.flush()

	session.add( tc1 )
	session.add( tc2 )

	session.commit()

	print '===========================', 'Buildings', '==========================='	

	q = session.query( Building.id )
	for i in q:
		print i

	print '===========================', 'Units', '==========================='

	q = session.query( Unit.id )
	for i in q:
		print i

	"""