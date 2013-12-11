# SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.sql.expression import func, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_fulltext import FullText, FullTextSearch
import sqlalchemy_fulltext.modes as FullTextMode
import datetime

Base = declarative_base()

class Unit( FullText, Base ):
	__tablename__ = 'property__unit'
	__table_args__ = {'mysql_engine':'MyISAM'}

	id 				= Column( Integer, primary_key=True )

	address_id 		= Column( Integer, ForeignKey( 'loc__address.id' ) )
	address   		= relationship( 'Address' )

	property_id 	= Column( Integer, ForeignKey( 'property.id' ) )
	building   		= relationship( 'Building' )

	#leases 		= relationship( 'Lease' )
	price 			= Column( Float, default=0 )

	manager_access 	= relationship( 'Property_Access' )
	#invoices 		= relationship( 'Invoice' )


class Property_Access( FullText, Base ):
	__tablename__ = 'property__access'
	__table_args__ = {'mysql_engine':'MyISAM'}

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


class Lease( FullText, Base ):
	__tablename__ = 'property__unit__lease'
	__table_args__ = {'mysql_engine':'MyISAM'}

	id 						= Column( Integer, primary_key=True )

	unit_id 				= Column( Integer, ForeignKey( 'property__unit.id' ) )
	unit 					= relationship( 'Unit', backref=backref('lease') )

	recurring_invoice_id 	= Column( Integer, ForeignKey( 'payment__invoice__recurring.id' ) )
	recurring_invoice 		= relationship( 'Recurring_Invoice' )

	#members 				= relationship( 'Tenant', primaryjoin='Lease.id==Tenant.lease_id' )
	#defunct_members			= relationship( 'Tenant', primaryjoin='Lease.id==Tenant.lease_defunct_id' )

	defunct 				= Column( Boolean, default=False )

class Building( FullText, Base ):
	__tablename__ = 'property'
	__table_args__ = {'mysql_engine':'MyISAM'}

	id 			= Column( Integer, primary_key=True )
	#address_id = Column( Integer, ForeignKey( 'loc__address.id' ) )

class Invoice( FullText, Base ):
	__tablename__ = 'payment__invoice'
	__table_args__ = {'mysql_engine':'MyISAM'}

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
	description 				= Column( String(512), default='' )
	note 						= Column( String(512), default='' )

	is_template 				= Column( Boolean, default=False )
	available_balance 			= Column( Float, default=0 )
	account_number 				= Column( String( length=256 ), default=None )


class Recurring_Invoice( FullText, Base ):
	__tablename__ = 'payment__invoice__recurring'
	__table_args__ = {'mysql_engine':'MyISAM'}

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


class Invoice_Payer( FullText, Base ):
	__tablename__ = 'payment__invoice__payer'
	__table_args__ = {'mysql_engine':'MyISAM'}

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


class Property_Manager( FullText, Base ):
	__tablename__ = 'property__manager'
	__table_args__ = {'mysql_engine':'MyISAM'}

	id 				= Column( Integer, primary_key=True )

	#account_id 	= Column( Integer, ForeignKey( 'payment__account.id' ) )
	#account 		= relationship( 'Payment_Account' )

	master_manager 	= Column( Boolean, default=False )
	status 			= Column( Enum( 'unknown', 'pending_denial', 'denied', 'verified', 'payments_blocked' ), default='unknown' ) 

	num_units 		= Column( Integer )

class Address( FullText, Base ):
    __tablename__ = 'loc__address'
    __table_args__ = {'mysql_engine':'MyISAM'}

    id               = Column( Integer, primary_key=True )
    street_number    = Column( String(10) )
    street_str       = Column( String(128) )
    internal_address = Column( String(50) )
    city_str         = Column( String(129) )
    zipcode_str      = Column( String(5) )
    state_str        = Column( String(2) )
    image_cache_url  = Column( String(512) )
    image_source_url = Column( String(512) )

    @hybrid_property
    def street_address(self):
        return ((self.street_number + ' ') if self.street_number else '') + self.street_str

    @hybrid_property
    def city_state_zip(self):
        return self.city_str.title() + ', ' + self.state_str + ' ' + self.zipcode_str

class Account_Profile( FullText, Base ):
	__tablename__ = 'account__profile'
	__table_args__ = {'mysql_engine':'MyISAM'}

	id = Column( Integer, primary_key=True)

	#user_id 				= Column( Intger, ForeignKey('user__table.id') )

	first_name 				= Column( String(32) )
	last_name  				= Column( String(32) )
	company    				= Column( String(56) )

	work_number 			= Column( String(16) )
	home_number				= Column( String(16) )
	mobile_number 			= Column( String(16) )

	contact_email 			= Column( String(64) )

	address_id 				= Column( Integer, ForeignKey('loc__address.id') )
	address 				= relationship( 'Address', foreign_keys=[address_id] )

	billing_address_name 	= Column( String(56) )
	billing_address_id 		= Column( Integer, ForeignKey('loc__address.id') )
	billing_address			= relationship( 'Address', foreign_keys=[billing_address_id] )	

	accepted_terms 			= Column( Boolean, default=False )


_session = sessionmaker()
_engine = create_engine( 'mysql+pymysql://root:testtest@localhost/rentshare_test1' )
_session.configure( bind=_engine )

session = _session()

#_engine.dialect.has_table( _engine.connect(),
#                                         TABLE_NAME ) == False:
Base.metadata.create_all( _engine )


addy1 = Address(street_number=123, street_str='street road', city_str='here')
addy2 = Address(street_number=456, street_str='street road', city_str='here')
addy3 = Address(street_number=7, street_str='broadway', city_str='new york')

session.flush()

ap1 = Account_Profile(first_name='street', address = addy1)
ap2 = Account_Profile(first_name='henry', address = addy2)
ap3 = Account_Profile(first_name='broadway', address = addy3)

session.add_all([addy1, addy2, addy3, ap1, ap2, ap3])
session.commit()


qry = session.query(Address, Account_Profile)\
	.filter(Address.id == Account_Profile.address_id)\
	.filter(FullTextSearch('+456 +Street', [Address.street_number, Address.street_str, Account_Profile.first_name], mode=FullTextMode.BOOLEAN))
#qry = session.query(Address).filter(FullTextSearch('+456 +Street', Address, mode=FullTextMode.BOOLEAN))

for i in qry:
	print i[0].street_number, i[0].street_str, i[1].first_name