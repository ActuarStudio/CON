from pprint import pprint
import pandas as pd
from lxml import etree
from io import StringIO
import sys
import traceback

####################################

ERRFREE_OFF = True


# -----------   Работа с ошибками ------------------

def ERRSELF(f):
    def ff(self,*args,**kwargs):
        if self.err_critical:
            return self
        else:
            return f(self,*args,**kwargs)

    return ff


def ERRNONE(f):
    def ff(self,*args,**kwargs):
        if self.err_critical:
            return None
        else:
            return f(self,*args,**kwargs)

    return ff

# -----------   Работа с ошибками ------------------

def ERRFREE(f):
    if ERRFREE_OFF: return f

    def ff(self,*args,**kwargs):
        p = f.__name__
        try:
            return f(self,*args,**kwargs)
        # except Exception as ex:
        except (ArithmeticError, LookupError, UserError, etree.XMLSyntaxError,
                ReferenceError,AttributeError,NameError, UnicodeError,OSError,
                TypeError, ValueError) as ex:

            exc_type, exc_value, exc_traceback = sys.exc_info()

            self.err_critical = True
            self.err_plase = p
            self.err_type = exc_type.__name__  # или ex.__class__.__name__
            self.err_cod = exc_value.__str__()  # или str(ex)
            self.err_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

            # после отладки убрать !!!!!!!!!!!!!!!!!

            print(ERRTEXT(self.err_plase, self.err_point, self.err_type, self.err_cod, self.err_trace))

            return self

    return ff

class UserError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr(self.value)

# после отладки убрать !!!!!!!!!!!!!!!!

def ERRTEXT(plase, point, type, cod, trace):
    s = f'Критична помилка.\nФункція {plase}\nТочка {point}\nТип {type}\nКод {cod}\nТрасса {trace}'
    return s



# -----------  Конец Работа с ошибками ------------

####################################


IR2_schema  = 'static/tir2.xsd'
IR4_schema  = 'static/tir4.xsd'
IR71_schema = 'static/tir71.xsd'
IR91_schema = 'static/tir91.xsd'
FR0_schema  = 'static/tfr0.xsd'
NBU_schema  = 'static/nbu0.xsd'
KOD11       = 'static/kod11.xlsx'

class NBUXML_base:

    def __init__(self, reporting_period=None, edrpou=None):

        self._IR2_schema = IR2_schema
        self._IR4_schema = IR4_schema
        self._IR71_schema= IR71_schema
        self._IR91_schema= IR91_schema
        self._FR0_schema = FR0_schema
        self._NBU_schema = NBU_schema
        self._KOD11      = KOD11
        self._Delta_precision  = Delta_precision

        self.err_critical  = False
        self.err_place     = ''
        self.err_file      = ''
        self.err_resource  = ''
        self.err_cod       = ''
        self.err_point     = ''
        self.err_trace     = ''

        self.reporting_period = reporting_period
        self.reporting_date = None
        self.edrpou  = str(edrpou)

    @ERRSELF
    @ERRFREE
    def _set_date( self ):

        d = self.reporting_period

        if pd.isna(d):
            d = pd.to_datetime("now")
            p = pd.Period(d, freq='Q')
            d = p.start_time.floor(freq='D')
            p = p-1
            self.reporting_date = d.strftime('%d.%m.%Y')
            self.reporting_period = p
            return self

        if isinstance(d, pd.Period):
            p = pd.Period(d, freq='Q')
        else:
            p = pd.to_datetime(d, errors="coerce", dayfirst=True)
            if pd.isna(p) :                    raise UserError('err001')
            p = pd.Period(p, freq='Q')
            d = (p+1).start_time.floor(freq='D')
            self.reporting_date = d.strftime('%d.%m.%Y')
            self.reporting_period = p
            return self

    @ERRNONE
    @ERRFREE
    def _xml2df(self, xml=None, sch1=None, sch2=None ):

        if pd.isna(xml) : return None

        self.err_resource = xml

        self.err_point = '101'
        tree = etree.parse(xml)
        root = tree.getroot()

        self.err_point = '102'
        schema_tree = etree.parse(sch1)
        schema_root = schema_tree.getroot()
        schema = etree.XMLSchema(schema_root)

        self.err_point = '103'
        if not schema.validate(tree):    raise UserError('err103')

        self.err_point = '104'
        schema_tree = etree.parse(sch2)
        schema_root = schema_tree.getroot()
        schema = etree.XMLSchema(schema_root)

        self.err_point = '105'
        if not schema.validate(tree):
            pprint(schema.error_log)
            raise UserError('err105')

        self.err_point = '106'
        if root.tag != 'NBUSTATREPORT': raise UserError('err106')

        self.err_point = '107'
        head = root.find('HEAD')
        if head is None:                raise UserError('err107')

        statform   = head.find('STATFORM')
        edrpou     = head.find('EDRPOU')
        reportdate = head.find('REPORTDATE')
        if statform is None or edrpou is None or reportdate is None: raise UserError('err107')

        statform   = statform.text
        edrpou     = edrpou.text
        reportdate = reportdate.text
        if statform is None or edrpou is None or reportdate is None: raise UserError('err107')

        self.err_point = '108'
        if (statform[:3] !='FIR') and (statform[:3] !='FFR'):        raise UserError('err108')
        self.err_point = '109'
        if (edrpou!=self.edrpou) :                                   raise UserError('err109')
        self.err_point = '110'
        if (reportdate != self.reporting_date):                      raise UserError('err110')

        self.err_point = '111'
        all_records = []
        for data in root.iterchildren(tag="DATA"):
            record = {}
            for subdata in data:
                record[subdata.tag] = subdata.text
            all_records.append(record)

        df = pd.DataFrame(all_records,dtype='string')

        self.err_point = ''
        self.err_resource = ''
        return df

    @ERRSELF
    @ERRFREE
    def _df2xml(self, df=None, xmlname=None, date=None, edrpou=None, nbucod=None):

        self.err_resource = xmlname

        self.err_point = '301'
        root = etree.Element('NBUSTATREPORT');
        comment = etree.Comment(text='  actuar.online  ')
        root.addprevious(comment)

        head = etree.SubElement(root, 'HEAD')

        #statform = etree.SubElement(head, 'STATFORM')
        #statform.text = nbucod
        etree.SubElement(head, 'STATFORM').text = nbucod
        etree.SubElement(head, 'EDRPOU').text = edrpou
        etree.SubElement(head, 'REPORTDATE').text = date

        self.err_point = '302'
        for i, row in df.iterrows():
            data = etree.SubElement(root, 'DATA')
            for column in df.columns:
                #item = etree.SubElement(data, column)
                #item.text = str(row.loc[column])
                etree.SubElement(data, column).text = str(row.loc[column])
        tree = etree.ElementTree(root)

        self.err_point = '303'
        tree.write(xmlname, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=True)

        s = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=True).decode("UTF-8")


        self._xml = s
        # pprint (s)

        self.err_point = ''
        self.err_resource = ''
        return self

    # import codecs
    # if s[:3] == codecs.BOM_UTF8:
    #    print('УРАААААА')
    # print(s[:3])
    # content = content[3:]
    from codecs import open
    # with open(xmlname, 'wb') as f:
    #    f.write(s)

    @ERRSELF
    @ERRFREE
    def set_period ( self, ir4=None,ir2=None,fr0=None,ir71=None ):

        df0 = pd.DataFrame({}, columns=['EKP', 'H011', 'T100', 'T100_2', 'T070'])
        self.full_df = df0
        self.ir4_df  = df0
        self.ir2_df  = df0
        self.ir71_df = df0
        self.fr0_df  = df0

        self._set_date()
        if self.err_critical : return self

        date = self.reporting_date
        edrpou = self.edrpou

        if pd.notna(ir4) :
            df = self._xml2df(xml=ir4, sch1=self._NBU_schema, sch2=self._IR4_schema)
            if self.err_critical: return self
            else : self.ir4_df = df

        if pd.notna(ir2):
            df = self._xml2df(xml=ir2, sch1=self._NBU_schema, sch2=self._IR2_schema)
            if self.err_critical: return self
            else  : self.ir2_df = df

        if pd.notna(ir71):
            df = self._xml2df(xml=ir71, sch1=self._NBU_schema, sch2=self._IR71_schema)
            if self.err_critical: return self
            else  : self.ir71_df = df

        if pd.notna(fr0):
            df  = self._xml2df(xml=fr0, sch1=self._NBU_schema, sch2=self._FR0_schema)
            if self.err_critical: return self
            else :  self.fr0_df = df

        self.err_point = '201'

        db = pd.DataFrame({}, columns=['edrpou', 'date', 'class', 'cod', 'value'])

        lst = ['IR40001','IR40002','IR40003','IR40004','IR40007','IR40008','IR40015','IR40016','IR40017','IR40018','IR40019',
               'IR40024','IR40025','IR40026','IR40029','IR40032','IR40035','IR40038','IR40043','IR40048','IR40053','IR40060']

        d4 = self.ir4_df

        if len(d4.index)>0:

            d4 = d4.loc[d4['EKP'].isin(lst)]
            d4 = d4.astype({'T100':'int64'}).astype({'T100':'Int64'})

            #dfg = df.groupby(['EKP', 'H011'], as_index=True).agg(
            #    sum=pd.NamedAgg(column='T100', aggfunc='sum'))
            d4 = d4.groupby(['EKP', 'H011'], as_index=False)[['T100']].sum()

            db['class'] = d4['H011'].astype(str).astype('string')
            db['cod']   = d4['EKP'].astype(str).astype('string')
            db['value'] = d4['T100'].astype('int64').astype('Int64')
            db['edrpou']= self.edrpou        #тіп
            db['date'] =  self.reporting_date #тіп

        self.err_point = '202'

        dd = self.fr0_df.loc[self.fr0_df['EKP']=='FR001060',['T100_2']].astype('int64').astype('Int64')
        if len(dd.index) > 0:
            val = dd.iat[0,0] #dd['T100_2'].iat[0]   .iloc[0]
            print ('ЕСТЬ ДАК !!!')
            print (val)
        else:
            val = 0
        x ={'edrpou':self.edrpou,'date':self.reporting_date,'class':'00','cod':'FR001000','value':val}

        db = db.append({'edrpou':self.edrpou,'date':self.reporting_date,
                       'class':'00','cod':'FR001000','value':val},ignore_index=True)

        self.err_point = '203'

        dd = pd.DataFrame({},columns=['edrpou','date','class','cod','value'])

        if len(self.ir71_df.index) > 0:

            dd['cod']   = self.ir71_df['EKP'].astype(str).astype('string')
            dd['value'] = self.ir71_df['T070'].astype('int64').astype('Int64')
            dd['edrpou']= self.edrpou         #тіп
            dd['date'] =  self.reporting_date #тіп
            dd['class'] = '00'

        if len(dd.index) > 0:
            db = db.append(dd,ignore_index=True)

        self.err_point = '204'

        dd = pd.DataFrame({}, columns = ['edrpou', 'date', 'class', 'cod', 'value'])

        if len(self.ir2_df.index) > 0:

            dd['cod']   = self.ir2_df['EKP'].astype(str).astype('string')
            dd['value'] = self.ir2_df['T070'].astype('int64').astype('Int64')
            dd['edrpou']= self.edrpou        #тіп
            dd['date'] =  self.reporting_date #тіп
            dd['class'] = '00'
            lst = ['IR20009','IR20040','IR20001','IR20049','IR20052','IR20057','IR20050','IR20063']
            dd = dd.loc[dd['cod'].isin(lst)]

        if len(dd.index) > 0:
            db = db.append(dd,ignore_index=True)

        self.err_point = '205'
        self.full_df = db

        self._check_db()
        if self.err_critical: return self

        self.err_point = ''
        return self

    @ERRSELF
    @ERRFREE
    def get_xml91 (self,df,fname):

        self._set_date()
        if self.err_critical: return self

        self.err_point = '401'
        self.err_resource = ''

        cl = ['EKP','H011','T070']

        if not isinstance(df, pd.DataFrame): raise UserError('err401')
        cl2 = df.columns
        if not set(cl).issubset(cl2):       raise UserError('err401')
        df1 = pd.DataFrame(df,columns=cl,dtype="string")
        self.ir91_df_str = df1

        self.err_point = '402'
        self.err_resource = fname
        self._df2xml(df=df1, xmlname=fname, date=self.reporting_date, edrpou=self.edrpou, nbucod='FIR91')

        self.err_point = '403'
        tree = etree.parse(fname)
        root = tree.getroot()

        self.err_point = '404'
        schema_tree = etree.parse(self._NBU_schema)
        schema_root = schema_tree.getroot()
        schema = etree.XMLSchema(schema_root)

        self.err_point = '405'
        if not schema.validate(tree):    raise UserError('err405')

        self.err_point = '406'
        schema_tree = etree.parse(self._IR91_schema)
        schema_root = schema_tree.getroot()
        schema = etree.XMLSchema(schema_root)

        self.err_point = '407'
        if not schema.validate(tree):
            print(schema.error_log)
            raise UserError('err407')

        self.err_point = '408'
        #if hasattr(self, '_xml'):
        self.ir91_xml_str = self._xml

        self.err_point = ''
        self.err_resource = ''
        return self

    @ERRNONE
    @ERRFREE
    def get_db_df(self):
        self.err_point = '501'
        self.err_resource = ''

        s = self.full_df

        self.err_point = ''
        return s

    @ERRSELF
    @ERRFREE
    def get_db_xls(self,fname='00db.xlsx'):

        self.err_point = '601'
        self.err_resource = fname

        info = [['EDRPOU',self.edrpou],['REPORTING_DATE',self.reporting_date]]
        info = pd.DataFrame(info,columns=['Показник','Значення'])
        with pd.ExcelWriter(fname) as writer:
            info.to_excel(writer, sheet_name='info')
            self.full_df.to_excel(writer, sheet_name='db_full')

        self.err_point = ''
        self.err_resource = ''
        return self

    @ERRSELF
    @ERRFREE
    def _check_db(self):

        self.err_point = '701'
        self.err_resource = ''

        s = self.full_df.copy()

        g = s.groupby(['cod'], as_index=False)[['value']].sum()
        g = g.set_index('cod')
        l = list(g.index)
        def gv(g,l,x): return (g.at[x,'value'] if (x in l) else 0)

        IR20001 = gv(g,l,'IR20001')
        IR20009 = gv(g,l,'IR20009')
        IR20040 = gv(g,l,'IR20040')
        IR20049 = gv(g,l,'IR20049')
        IR20050 = gv(g,l,'IR20050')
        IR20052 = gv(g,l,'IR20052')
        IR20057 = gv(g,l,'IR20057')
        IR20063 = gv(g,l,'IR20063')
        IR40001 = gv(g,l,'IR40001')
        IR40003 = gv(g,l,'IR40003')
        IR40007 = gv(g,l,'IR40007')
        IR40008 = gv(g,l,'IR40008')
        IR40015 = gv(g,l,'IR40015')
        IR40016 = gv(g,l,'IR40016')
        IR40017 = gv(g,l,'IR40017')
        IR40018 = gv(g,l,'IR40018')
        IR40019 = gv(g,l,'IR40019')
        IR40024 = gv(g,l,'IR40024')
        IR40026 = gv(g,l,'IR40026')
        IR40027 = gv(g,l,'IR40027')
        IR40032 = gv(g,l,'IR40032')
        IR40033 = gv(g,l,'IR40033')
        IR40035 = gv(g,l,'IR40035')
        IR40038 = gv(g,l,'IR40038')
        IR40043 = gv(g,l,'IR40043')
        IR40060 = gv(g,l,'IR40060')

        '''
        IR40007 = IR20009
        IR40026 + IR40027 = IR20040
        IR40001 - IR40003 = IR20001
        IR40032 = IR20049
        IR40035 = IR20052
        IR40038 = IR20057
        IR40033 = IR20050
        IR40043 = IR20063
        IR40015 = IR40016 + IR40017 + IR40018 + IR40019
        IR40008 <= IR40007
        IR40024 <= IR40015
        IR40060 <= IR40016        
        '''

        delta = self._Delta_precision

        db_err = pd.DataFrame({},columns=['Text','L','R','Delta','Err'])

        text = 'IR40007 = IR20009'
        l = IR40007
        r = IR20009
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40026 + IR40027 = IR20040'
        l = IR40026+IR40027
        r = IR20040
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40001 - IR40003 = IR20001'
        l = IR40001 - IR40003
        r = IR20001
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40032 = IR20049'
        l = IR40032
        r = IR20049
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40035 = IR20052'
        l = IR40035
        r = IR20052
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40038 = IR20057'
        l = IR40038
        r = IR20057
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40033 = IR20050'
        l = IR40033
        r = IR20050
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40043 = IR20063'
        l = IR40043
        r = IR20063
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40015 = IR40016 + IR40017 + IR40018 + IR40019'
        l = IR40015
        r = IR40016 + IR40017 + IR40018 + IR40019
        val = abs(l-r)
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40008 <= IR40007'
        l = IR40008
        r = IR40007
        val = l-r
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40024 <= IR40015'
        l = IR40024
        r = IR40015
        val = l-r
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        text = 'IR40060 <= IR40016'
        l = IR40060
        r = IR40016
        val = l-r
        db_err=db_err.append( {'Text':text,'L':l,'R':r,'Delta':val,'Err':val>delta},ignore_index=True)

        self.full_df_err = db_err

        self.err_point = ''
        return


#######################################


cred = credentials.Certificate('HELP/blog-c5e87-firebase-adminsdk-1yuvu-e59ced0984.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'test').document(u'doc1')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

users_ref = db.collection(u'test')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')



#######################################