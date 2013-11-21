# SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.sql.expression import func, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
import datetime

Base = declarative_base()

class Unit( Base ):
	__tablename__ = 'property__unit'

	id 				= Column( Integer, primary_key=True )

	#address_id 	= Column( Integer, ForeignKey( 'loc__address.id' ) )
	#address   		= relationship( 'Address' )

	property_id 	= Column( Integer, ForeignKey( 'property.id' ) )
	building   		= relationship( 'Building' )

	#leases 		= relationship( 'Lease' )
	price 			= Column( Float, default=0 )

	manager_access 	= relationship( 'Property_Access' )
	#invoices 		= relationship( 'Invoice' )


class Property_Access( Base ):
	__tablename__ = 'property__access'

	id 					= Column( Integer, primary_key=True )

	property_id 		= Column( Integer, ForeignKey( 'property.id' ) )
	building   			= relationship( 'Building' )

	unit_id 			= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 				= relationship( 'Unit' )

	manager_id 			= Column( Integer, ForeignKey( 'property__manager.id' ) )
	manager 			= relationship( 'Property_Manager' )

	#manager_type_id 	= Column( Integer, ForeignKey( 'property__access__type.id' ) )
	#manager_type 		= relationship( 'Manager_Type' )

	receiver 			= Column( Integer, default=False )
	status 				= Column( Enum( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' )


class Lease( Base ):
	__tablename__ = 'property__unit__lease'

	id 						= Column( Integer, primary_key=True )

	unit_id 				= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 					= relationship( 'Unit', backref=backref('lease') )

	recurring_invoice_id 	= Column( Integer, ForeignKey( 'payment__invoice__recurring.id' ) )
	recurring_invoice 		= relationship( 'Recurring_Invoice' )

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

	payers 						= relationship( 'Invoice_Payer' )
	#items 						= relationship( 'payment__invoice__item' )
	#item_amounts 				= relationship( 'payment__invoice__item__payer__amount' )

	parent_recurring_invoice_id = Column( Integer, ForeignKey( 'payment__invoice__recurring.id' ) )
	recurring_invoice 			= relationship( 'Recurring_Invoice' )

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

	is_template 				= Column( Boolean, default=False )
	available_balance 			= Column( Float, default=0 )
	account_number 				= Column( String( length=256 ), default=None )


class Recurring_Invoice( Base ):
	__tablename__ = 'payment__invoice__recurring'

	id 					= Column( Integer, primary_key=True )

	#invoice_id  		= Column( Integer, ForeignKey( 'payment__invoice.id' ) )
	invoices 		 	= relationship( 'Invoice' )

	cycle_offset 		= Column( Integer, default=1 )
	#cycle_freq			= Column( Integer, default=1 )
	due_offset			= Column( Integer, default=0 )

	service_start_date 	= Column( Date )
	service_end_date	= Column( Date )
	creation_date 		= Column( Date, default=func.current_timestamp() )


	prepay 				= Column( Boolean, default=False )
	#autopayers			= relationship( 'Payment_Invoice_Recurring_Autopayer' )
	
	defunct 			= Column( Boolean, default=False )
	defunct_date		= Column( Date )


class Invoice_Payer( Base ):
	__tablename__ = 'payment__invoice__payer'

	id 							= Column( Integer, primary_key=True )

	#account_id 					= Column( Integer, ForeignKey( 'payment__account.id' ) )
	#account 					= relationship( 'Payment_Account' )

	invoice_id 					= Column( Integer, ForeignKey('payment__invoice.id') )
	invoice 					= relationship( 'Invoice' )

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
	status 			= Column( Enum( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' ) 

	num_units 		= Column( Integer )


_session = sessionmaker()
_engine = create_engine( 'sqlite:///_rentshare_test.db' )
_session.configure( bind=_engine )

#_engine.dialect.has_table( _engine.connect(),
#                                         TABLE_NAME ) == False:
Base.metadata.create_all( _engine )

if __name__ == '__main__':
	session = _session()

	if False:

		#make some dummy units
		u1 = Unit()
		u2 = Unit()
		u3 = Unit()

		#make some dummy property accesses
		pa1 = Property_Access( status='verified' )
		pa2 = Property_Access()
		pa3 = Property_Access()

		#make some dummy managers
		m1 = Property_Manager( master_manager=True, status='verified', num_units = 10 )
		m2 = Property_Manager( master_manager=True, status='unknown', num_units = 43 )

		#make some dummy recurring invoices
		ri1 = Recurring_Invoice()
		ri2 = Recurring_Invoice()
		ri3 = Recurring_Invoice()

		#make some dummy invoices
		inv1 = Invoice( recurring_invoice=ri1 )
		inv2 = Invoice( recurring_invoice=ri2 )
		inv3 = Invoice( recurring_invoice=ri3 )

		#make some dummy invoice payers
		ip1 = Invoice_Payer( invoice=inv1, amount_paid=100 )
		ip2 = Invoice_Payer( invoice=inv2, amount_paid=0 )
		ip3 = Invoice_Payer( invoice=inv3, amount_paid=369 )

		#make some dummy leases
		lease1 = Lease( unit=u1, recurring_invoice=ri1 )
		lease2 = Lease( unit=u2, recurring_invoice=ri2 )
		lease3 = Lease( unit=u3, recurring_invoice=ri3 )

		session.flush()
		
		
		u1.manager_access.append(pa1)
		u2.manager_access.append(pa2)
		u3.manager_access.append(pa3)

		pa1.manager = m1
		pa2.manager = m2
		pa3.manager = m2
		
		session.add_all([u1, u2, u3, pa1, pa2, pa3, m1, m2, inv1, inv2, inv3, ip1, ip2, ip3])
		session.commit()

	#end making dummy values

	qry = session.query( Unit )\
		.join( Property_Access, Property_Access.unit_id == Unit.id )\
		.join( Lease, Lease.unit_id == Unit.id )\
		.join( Recurring_Invoice, Lease.recurring_invoice_id == Recurring_Invoice.id )\
		.join( Invoice, Invoice.parent_recurring_invoice_id == Recurring_Invoice.id )\
		.join( Invoice_Payer, Invoice_Payer.invoice_id == Invoice.id )\
		.filter( Invoice_Payer.amount_paid > 0 )\
		.order_by( case( [(Property_Access.status == 'unknown', 0) ], else_=1 ))

	print '======================================================'
	for i in qry:
		print 'Unit: ', i.id
		print 'Access Status: ', i.manager_access[0].status
		print 'Amount Paid: ', i.lease[0].recurring_invoice.invoices[0].payers[0].amount_paid
		print '======================================================'


	if False:

		qry = session.query(Unit, Property_Access, Property_Manager)\
			.order_by( Property_Manager.status )\
			.filter( Property_Access.status == 'unknown' )\
			.filter( Property_Manager.id == Property_Access.manager_id )\
			.filter( Unit.id == Property_Access.unit_id )

		for i in qry:
			print 'Unit: ', i[0].id, ' ===  Property Access: ', i[1].id, ' ===  Property Manager: ', i[2].id
		
		print '\n================================================================================'

		qry = session.query( Unit )\
			.join( Property_Access, Property_Access.unit_id == Unit.id )\
			.join( Property_Manager, Property_Manager.id == Property_Access.manager_id )\
			.order_by( Property_Manager.status )\
			.filter( Property_Access.status == 'unknown' )

		for i in qry:
			print 'Unit: ', i.id, ' ===  Property Access: ', i.manager_access[0].id, ' ===  Property Manager: ', i.manager_access[0].manager.id

	#end test queries