
from collections import defaultdict


class CDRDataInfo:
    """
    Simple class for holding and accessing Cluster and Length data for a particular Decoy.
    """
    def __init__(self, name, strategy, decoy):
        self.name = name
        self.strategy = strategy
        self.decoy = decoy

        self.data = defaultdict()
        self.cdrs = ["L1", "L2", "L3", "H1", "H2", "H3"]

    def __repr__(self):
        line = ""
        for cdr in self.cdrs:
            if self.data.has_key(cdr):
                line = line + cdr+":"+repr(self.get_value_for_cdr(cdr))
        line = line+"\n"
        #print line
        return line

    def get_data(self):
        return self.data

    def get_value_for_cdr(self, cdr):
        return self.data[cdr]

    def set_value_for_cdr(self, cdr, value):
        self.data[cdr] = value

    def set_data(self, data):
        """
        Dictionary for each CDR: L1, L2, L3, H1, H2, H3
        """
        self.data = data

    def set_value(self, cdr, value):
        self.data[cdr] = value

    def get_data_tuple(self):
        """
        Return tuple with data at each position: [L1, L2, L3, H1, H2, H3]
        If Camelid, will only return H data.
        """

    def has_data(self, cdr):
        if self.data.has_key(cdr):
            return True
        else:
            return False

    def is_camelid(self):
        """
        Return True if missing light chain data
        """
        if (not self.has_data('L1')) and (not self.has_data('L2')) and (not self.has_data('L3')):
            return True
        else:
            return False

class CDRData:
    """
    Class holding cluster and length data from cluster or antibody features database.
    """
    def __init__(self, name, native_path, is_camelid = False):
        self.is_camelid = is_camelid
        self.name = name

        self.all_data = defaultdict()
        if is_camelid:
            self.cdrs = ["H1", "H2", "H3"]
        else:
            self.cdrs = ["L1", "L2", "L3", "H1", "H2", "H3"]


        self.native_data = None
        self._setup_native_data(native_path)

    def _get_stmt(self, column_name):
        if not self.is_camelid:
            stmt = "SELECT "+ \
                        "structures.input_tag as decoy,"+ \
                        "H1."+column_name+" as H1," +\
                        "H2."+column_name+" as H2," +\
                        "H3."+column_name+" as H3," +\
                        "L1."+column_name+" as L1," +\
                        "L2."+column_name+" as L2," +\
                        "L3."+column_name+" as L3"

            stmt = stmt + """
                    FROM
                        cdr_clusters as L1,
                        cdr_clusters as L2,
                        cdr_clusters as L3,
                        cdr_clusters as H1,
                        cdr_clusters as H2,
                        cdr_clusters as H3,
                        structures
                    WHERE
                        structures.struct_id = L1.struct_id AND
                        structures.struct_id = L2.struct_id AND
                        structures.struct_id = L3.struct_id AND
                        structures.struct_id = H1.struct_id AND
                        structures.struct_id = H2.struct_id AND
                        structures.struct_id = H3.struct_id AND
                        L1.CDR = 'L1' AND
                        L2.CDR = 'L2' AND
                        L3.CDR = 'L3' AND
                        H1.CDR = 'H1' AND
                        H2.CDR = 'H2' AND
                        H3.CDR = 'H3'
                    """
        else:
            stmt = "SELECT "+ \
                        "structures.input_tag as decoy,"+ \
                        "H1."+column_name+" as H1," +\
                        "H2."+column_name+" as H2," +\
                        "H3."+column_name+" as H3"

            stmt = stmt + """
                    FROM
                        cdr_clusters as H1,
                        cdr_clusters as H2,
                        cdr_clusters as H3,
                        structures
                    WHERE
                        structures.struct_id = H1.struct_id AND
                        structures.struct_id = H2.struct_id AND
                        structures.struct_id = H3.struct_id AND
                        H1.CDR = 'H1' AND
                        H2.CDR = 'H2' AND
                        H3.CDR = 'H3'
                    """
        #print stmt
        return stmt

    def add_data(self, strategy, con):
        pass

    def get_strategy_data(self, strategy):
        return self.all_data[strategy]

    def get_strategy_data_for_decoy(self, strategy, decoy):
        return self.all_data[strategy][decoy]

    def _get_add_data(self, strategy, con, column_name):
        self.column_name = column_name

        data = defaultdict()
        cur = con.cursor()
        print "Adding "+column_name+" data for "+strategy
        for row in cur.execute(self._get_stmt(column_name)):
            #print repr(row)
            d = CDRDataInfo(self.name, strategy, row[0])
            d.set_value('H1', row[1])
            d.set_value('H2', row[2])
            d.set_value('H3', row[3])

            if not self.is_camelid:
                d.set_value('L1', row[4])
                d.set_value('L2', row[5])
                d.set_value('L3', row[6])
            data[row[0]] = d

            #print repr(d)

        self._add_data(strategy, data)

    def _add_data(self, strategy, decoy_data_map):
        """
        Add data in the form of a dict of decoy:DataTriple
        """
        if not self.all_data.has_key(strategy):
            self.all_data[strategy] = defaultdict()
        self.all_data[strategy] = decoy_data_map
        #print repr(decoy_data_map)

    def get_native_data(self):
        return self.native_data

    def _setup_native_data(self, pdb_path):
        if not pdb_path: return None

    def _set_native_data_from_rosetta(self, pdb_path):
        pass

    def set_native_data_input_tag(self, con, input_tag):
        self._set_native_data_input_tag(con, input_tag, self.column_name)

    def _set_native_data(self, data):
        self.native_data = data


    def _set_native_data_input_tag(self, con, input_tag, column_name):
        pass

    def get_concatonated_map(self, cdr = None, decoy_list = None):
        """
        Returns a defaultDic:
        Default:
            decoy: CDRDataInfo

        CDR to get back cdr_value, decoy for sorting on cdr_value
        """

        result_data = defaultdict()
        for strategy in self.all_data:
            for decoy in self.all_data[strategy]:
                if decoy_list and decoy not in decoy_list:
                    continue
                triple = self.all_data[strategy][decoy]
                if isinstance(triple, CDRDataInfo): pass

                if cdr:
                    result_data[(triple.get_value_for_cdr(cdr), decoy)] = triple
                else:
                    result_data[decoy] = triple

        return result_data