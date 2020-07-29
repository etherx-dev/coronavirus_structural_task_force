# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = [('C', ' 618 ', 'THR', None, (228.888, 188.18, 191.09600000000003))]
data['rota'] = [('A', ' 525 ', 'CYS', 0.03745435504379037, (162.144, 169.932, 153.375)), ('A', ' 552 ', 'LEU', 0.0943762466878062, (163.85400000000007, 159.08700000000005, 173.62)), ('A', ' 738 ', 'CYS', 0.0896704765616463, (203.55300000000005, 189.498, 184.132)), ('B', ' 114 ', 'THR', 0.21034805516567742, (145.49, 198.018, 145.554)), ('B', ' 282 ', 'ASN', 0.18775545170453428, (149.774, 171.82300000000006, 181.673)), ('B', ' 336 ', 'CYS', 0.021008858638109827, (189.18600000000006, 221.08100000000005, 145.567)), ('B', ' 379 ', 'CYS', 0.012204796803416684, (188.33, 201.91700000000006, 151.89)), ('B', ' 525 ', 'CYS', 0.0, (184.79000000000005, 218.44, 155.189)), ('B', ' 645 ', 'THR', 0.22444311175027964, (166.808, 215.147, 201.351)), ('C', ' 126 ', 'VAL', 0.2335382328093975, (209.03900000000004, 231.669, 156.149)), ('C', ' 294 ', 'ASP', 0.1479851041827914, (218.687, 206.919, 187.547)), ('C', ' 432 ', 'CYS', 0.0, (199.005, 176.164, 148.922)), ('C', ' 553 ', 'THR', 0.12918237407599953, (225.176, 173.1, 176.77200000000002)), ('C', ' 617 ', 'CYS', 0.009871559178612075, (227.326, 189.815, 191.971))]
data['cbeta'] = []
data['probe'] = [(' C  95  THR  HG1', ' C 264  ALA  N  ', -0.948, (225.946, 231.862, 170.361)), (' C 102  ARG  HB3', ' C 121  ASN  HA ', -0.679, (218.99, 232.889, 156.753)), (' A 119  ILE HG12', ' A 128  ILE HG12', -0.676, (203.607, 146.688, 151.39)), (' B 560  LEU  H  ', ' B 563  GLN HE21', -0.668, (195.907, 227.176, 176.334)), (' C 418  ILE  HA ', ' C 422  ASN HD22', -0.645, (185.173, 167.532, 140.907)), (' C 104  TRP  H  ', ' C 119  ILE  HB ', -0.635, (217.88, 225.786, 157.15)), (' C 134  GLN  HB2', ' C 164  ASN HD21', -0.635, (221.577, 222.567, 140.444)), (' B 402  ILE HD12', ' B 406  GLU  HB3', -0.621, (197.971, 195.709, 138.385)), (' C 201  PHE  HB3', ' C 229  LEU  HB3', -0.612, (207.743, 220.927, 157.393)), (' C 379  CYS  HA ', ' C 432  CYS  HB3', -0.609, (199.054, 178.771, 149.771)), (' A 841  LEU  HA ', ' C 588  THR HG21', -0.585, (220.457, 177.144, 182.378)), (' C 546  LEU HD11', ' C 573  THR HG21', -0.584, (211.495, 173.599, 169.24)), (' B 566  GLY  H  ', ' B 575  ALA  HB3', -0.58, (188.84, 221.135, 176.323)), (' A 501  ASN  O  ', ' A 506  GLN  NE2', -0.58, (182.073, 190.757, 126.889)), (' B 562  PHE  O  ', ' B 564  GLN  NE2', -0.579, (194.959, 224.976, 168.746)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.577, (217.995, 208.618, 186.547)), (' B 294  ASP  N  ', ' B 294  ASP  OD1', -0.565, (152.07, 200.42, 186.807)), (' B 675  GLN  O  ', ' B 690  GLN  NE2', -0.56, (148.181, 202.493, 208.511)), (' C 442  ASP  O  ', ' C 448  ASN  ND2', -0.56, (194.167, 170.038, 124.365)), (' A 359  SER  OG ', ' A 360  ASN  ND2', -0.559, (152.941, 174.582, 151.244)), (' C  90  VAL HG13', ' C 267  VAL HG23', -0.556, (221.407, 220.189, 166.226)), (' B 403  ARG  NH1', ' B 504  GLY  O  ', -0.553, (196.223, 190.869, 132.207)), (' C 196  ASN HD21', ' C 231  ILE HD11', -0.552, (211.821, 217.366, 155.699)), (' B  34  ARG  NH2', ' B 221  SER  OG ', -0.55, (138.565, 186.873, 178.294)), (' A 328  ARG  NH2', ' A 531  THR  O  ', -0.549, (159.889, 156.517, 161.011)), (' A 294  ASP  N  ', ' A 294  ASP  OD1', -0.549, (188.864, 149.825, 184.347)), (' B  96  GLU  O  ', ' B 186  PHE  N  ', -0.547, (124.781, 187.655, 173.455)), (' A1091  ARG  NH1', ' A1118  ASP  O  ', -0.544, (183.897, 181.472, 258.344)), (' B 777  ASN  OD1', ' B1019  ARG  NH1', -0.543, (183.946, 174.829, 209.628)), (' C 642  VAL HG22', ' C 651  ILE HG12', -0.541, (227.854, 195.563, 194.499)), (' C 747  THR  O  ', ' C 751  ASN  ND2', -0.541, (170.41, 199.632, 170.458)), (' B 376  THR HG23', ' B 378  LYS  HE2', -0.538, (187.18, 197.311, 144.805)), (' A 129  LYS  HG2', ' A 169  GLU  HG3', -0.537, (205.073, 148.242, 142.72)), (' A 106  PHE  HB2', ' A 117  LEU  HB3', -0.536, (196.407, 146.743, 151.063)), (' C 494  SER  OG ', ' C 495  TYR  N  ', -0.534, (185.882, 166.45, 127.707)), (' B 188  ASN  HA ', ' B 209  PRO  HA ', -0.532, (130.474, 183.88, 176.84)), (' C1146  ASP  N  ', ' C1146  ASP  OD1', -0.532, (191.069, 189.186, 279.574)), (' B 329  PHE  O  ', ' B 580  GLN  NE2', -0.53, (180.8, 227.96, 160.893)), (' C  64  TRP  HA ', ' C 266  TYR  HB3', -0.523, (227.882, 223.782, 171.203)), (' C 117  LEU HD21', ' C 128  ILE HD11', -0.521, (213.735, 223.539, 154.982)), (' B 902  MET  HE1', ' B1049  LEU HD13', -0.521, (169.988, 181.302, 237.325)), (' A  91  TYR  OH ', ' A 191  GLU  OE2', -0.519, (201.474, 141.972, 170.394)), (' B 444  LYS  H  ', ' B 499  PRO  HD3', -0.519, (197.732, 200.037, 120.584)), (' C 203  ILE HG13', ' C 226  LEU  HB2', -0.518, (207.375, 226.112, 164.282)), (' C 212  LEU HD21', ' C 215  ASP  HB2', -0.518, (225.525, 229.402, 183.066)), (' A 627  ASP  N  ', ' A 627  ASP  OD1', -0.517, (174.275, 147.843, 178.594)), (' C 271  GLN  OE1', ' C 273  ARG  NH1', -0.516, (219.276, 208.023, 175.318)), (' A1103  PHE  HZ ', ' H   1  NAG  H62', -0.515, (184.323, 161.738, 259.903)), (' C 409  GLN  HA ', ' C 414  GLN  HG2', -0.513, (185.311, 174.828, 145.75)), (' C  85  PRO  HA ', ' C 237  ARG  HA ', -0.513, (223.99, 214.147, 158.598)), (' C 381  GLY  HA3', ' C 430  THR HG23', -0.512, (200.309, 175.584, 157.023)), (' B 568  ASP  OD1', ' B 572  THR  OG1', -0.51, (188.445, 214.396, 181.993)), (' A 142  GLY  H  ', ' A 159  VAL HG11', -0.509, (205.124, 130.882, 145.279)), (' C 201  PHE  H  ', ' C 229  LEU  H  ', -0.508, (205.789, 219.755, 158.357)), (' A 115  GLN  NE2', ' A 130  VAL  O  ', -0.508, (196.693, 150.985, 142.165)), (' C 475  ALA  HB3', ' C 487  ASN  HB3', -0.508, (168.165, 156.212, 136.519)), (' C 102  ARG HH11', ' C 122  ASN  HB2', -0.508, (217.093, 236.354, 159.465)), (' B 476  GLY  HA3', ' B 487  ASN HD22', -0.506, (225.718, 186.927, 138.017)), (' B 454  ARG  HE ', ' B 491  PRO  HB2', -0.505, (213.715, 198.518, 138.525)), (' B 689  SER  OG ', ' B 690  GLN  N  ', -0.505, (144.861, 205.812, 204.83)), (' A 353  TRP  HZ3', ' A 355  ARG  HD2', -0.504, (160.316, 190.316, 146.364)), (' B 329  PHE  H  ', ' B 530  SER  HB2', -0.502, (179.402, 225.317, 161.182)), (' C 452  LEU HD23', ' C 492  LEU  HB3', -0.499, (185.725, 159.216, 132.079)), (' B 474  GLN  NE2', ' B 478  THR  OG1', -0.499, (228.003, 189.446, 137.324)), (' C  91  TYR  OH ', ' C 191  GLU  OE2', -0.498, (216.889, 225.687, 175.526)), (' C 229  LEU HD12', ' C 230  PRO  HD2', -0.498, (205.244, 221.584, 153.876)), (' A  45  SER  OG ', ' A 847  ARG  NH2', -0.497, (212.82, 165.02, 180.641)), (' B1028  LYS  NZ ', ' B1042  PHE  O  ', -0.496, (177.313, 185.84, 223.122)), (' B 796  ASP  N  ', ' B 796  ASP  OD1', -0.495, (163.142, 164.631, 239.71)), (' C 240  THR  OG1', ' C 241  LEU  N  ', -0.494, (223.608, 227.391, 159.205)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.494, (191.843, 194.955, 222.915)), (' C 394  ASN  ND2', ' C 516  GLU  OE2', -0.493, (204.752, 164.407, 156.824)), (' B1091  ARG  NH1', ' B1118  ASP  O  ', -0.488, (185.183, 189.622, 258.146)), (' C 195  LYS  HG3', ' C 202  LYS  HB3', -0.488, (208.52, 218.206, 164.728)), (' A 752  LEU HD11', ' A 990  GLU  HG2', -0.487, (199.258, 191.695, 167.086)), (' B 605  SER  OG ', ' B 606  ASN  N  ', -0.485, (149.31, 199.651, 198.943)), (' C 164  ASN  N  ', ' C 164  ASN  OD1', -0.484, (217.452, 224.602, 140.342)), (' B  85  PRO  HA ', ' B 237  ARG  HG2', -0.483, (142.878, 203.117, 159.335)), (' A 438  SER  HB3', ' A 509  ARG  HG3', -0.482, (171.651, 184.814, 132.046)), (' C 136  CYS  HB2', ' C 139  PRO  HG3', -0.479, (227.464, 225.989, 148.678)), (' C 104  TRP  HB2', ' C 119  ILE HD12', -0.477, (217.805, 224.131, 158.8)), (' A1028  LYS  NZ ', ' A1042  PHE  O  ', -0.477, (192.618, 177.442, 222.6)), (' A 605  SER  OG ', ' A 606  ASN  N  ', -0.476, (192.755, 146.207, 196.324)), (' A 486  PHE  O  ', ' A 487  ASN  ND2', -0.476, (167.449, 221.324, 137.36)), (' B 780  GLU  OE2', ' B1019  ARG  NH1', -0.474, (184.286, 175.428, 211.518)), (' A 848  ASP  N  ', ' A 848  ASP  OD1', -0.474, (213.73, 170.31, 188.175)), (' A 327  VAL HG11', ' A 528  LYS  HG3', -0.472, (165.937, 161.998, 157.725)), (' B 212  LEU HD22', ' B 215  ASP  H  ', -0.472, (128.941, 194.485, 180.068)), (' B 393  THR HG21', ' B 520  ALA  HB3', -0.471, (194.472, 217.62, 161.435)), (' A 837  TYR  HH ', ' C 592  PHE  H  ', -0.47, (217.194, 185.251, 185.927)), (' C 106  PHE  HD1', ' C 238  PHE  HB2', -0.47, (220.467, 219.474, 157.962)), (' A 172  SER  OG ', ' A 173  GLN  N  ', -0.47, (213.756, 148.895, 152.759)), (' A 127  VAL HG12', ' A 171  VAL HG22', -0.467, (210.067, 146.682, 145.792)), (' A 454  ARG HH22', ' A 469  SER  H  ', -0.467, (159.222, 203.671, 139.514)), (' C 353  TRP  O  ', ' C 466  ARG  NH2', -0.466, (197.298, 160.53, 141.694)), (' B1147  SER  N  ', ' C1147  SER  O  ', -0.466, (184.743, 186.781, 280.682)), (' C 625  HIS  HB3', ' C 628  GLN  HB2', -0.466, (223.285, 198.754, 178.476)), (' C 349  SER  OG ', ' C 452  LEU  O  ', -0.465, (189.973, 163.484, 134.028)), (' A 374  PHE  HA ', ' A 436  TRP  HB3', -0.465, (175.501, 180.084, 137.13)), (' A 415  THR  OG1', ' A 416  GLY  N  ', -0.464, (177.499, 201.712, 147.062)), (' B 878  LEU HD21', ' B1052  PHE  HB3', -0.463, (168.796, 173.558, 226.627)), (' A 319  ARG  NH1', ' A 592  PHE  O  ', -0.463, (178.29, 158.379, 184.268)), (' A 703  ASN  ND2', ' B 787  GLN  OE1', -0.461, (179.434, 158.073, 229.914)), (' A 578  ASP  OD2', ' A 581  THR  OG1', -0.461, (154.948, 158.785, 166.185)), (' B 191  GLU  HB2', ' B 206  LYS  HB2', -0.459, (139.452, 186.682, 173.131)), (' B1116  THR HG22', ' B1138  TYR  HD2', -0.457, (178.592, 193.299, 265.549)), (' B 278  LYS  HE3', ' B 286  THR  HB ', -0.456, (149.055, 182.054, 186.376)), (' B 319  ARG HH21', ' C 740  MET  HE2', -0.455, (173.169, 206.651, 182.987)), (' B 736  VAL HG11', ' B1004  LEU HD21', -0.455, (179.085, 174.459, 186.917)), (' B 381  GLY  HA3', ' B 430  THR HG23', -0.454, (190.548, 204.377, 158.292)), (' C 457  ARG  NH2', ' C 459  SER  O  ', -0.454, (182.079, 158.565, 146.665)), (' A 835  LYS  HA ', ' A 835  LYS  HD3', -0.453, (219.731, 181.006, 195.273)), (' C 194  PHE  HD1', ' C 203  ILE HG22', -0.452, (212.604, 223.214, 163.378)), (' B 626  ALA  O  ', ' B 634  ARG  NH2', -0.452, (152.669, 211.992, 181.648)), (' B  33  THR  OG1', ' B 219  GLY  O  ', -0.451, (141.185, 190.121, 182.571)), (' A 454  ARG  NH2', ' A 469  SER  O  ', -0.45, (160.179, 204.709, 139.064)), (' C 474  GLN  OE1', ' C 476  GLY  N  ', -0.45, (168.828, 152.809, 139.742)), (' B 100  ILE HG22', ' B 242  LEU HD22', -0.449, (125.213, 193.274, 163.033)), (' B 418  ILE  HA ', ' B 422  ASN  HB2', -0.449, (205.14, 197.062, 142.322)), (' A 134  GLN  O  ', ' A 160  TYR  OH ', -0.448, (195.439, 136.944, 141.445)), (' B 516  GLU  HB2', ' B 519  HIS  HE1', -0.448, (195.18, 211.51, 161.621)), (' B 424  LYS  HB2', ' B 424  LYS  HE2', -0.447, (205.86, 197.82, 149.348)), (' A1126  CYS  HB2', ' A1132  ILE HD13', -0.446, (167.118, 175.459, 258.445)), (' C 538  CYS  HB2', ' C 590  CYS  HB3', -0.446, (221.788, 183.398, 178.124)), (' A 599  THR  OG1', ' A 600  PRO  O  ', -0.446, (191.253, 152.733, 197.316)), (' C  34  ARG  HA ', ' C  34  ARG  HD3', -0.443, (216.394, 223.109, 178.953)), (' B 300  LYS  NZ ', ' B 306  PHE  O  ', -0.443, (153.558, 191.48, 192.78)), (' A 351  TYR  HE1', ' A 452  LEU  HB3', -0.442, (163.638, 198.698, 133.908)), (' C1084  ASP  N  ', ' C1084  ASP  OD1', -0.441, (202.441, 174.984, 266.089)), (' C 117  LEU HD13', ' C 231  ILE HD13', -0.441, (211.934, 219.759, 154.273)), (' C 104  TRP  HE1', ' C 265  TYR  HE1', -0.439, (221.195, 225.651, 163.728)), (' C 900  MET  HB3', ' C 900  MET  HE2', -0.438, (181.621, 203.116, 246.383)), (' C 439  ASN  O  ', ' C 443  SER  OG ', -0.438, (193.652, 177.226, 124.53)), (' B 560  LEU  O  ', ' B 577  ARG  NH2', -0.438, (194.823, 228.541, 173.205)), (' B 206  LYS  HG3', ' B 223  LEU  HG ', -0.436, (141.183, 182.835, 174.25)), (' A 710  ASN HD22', ' A1076  THR HG23', -0.435, (171.37, 162.458, 250.472)), (' B 992  GLN  H  ', ' B 992  GLN  HG2', -0.434, (180.872, 179.856, 164.826)), (' A 518  LEU  HA ', ' A 518  LEU HD12', -0.434, (163.365, 175.217, 164.382)), (' B 452  LEU HD13', ' B 492  LEU HD23', -0.434, (211.968, 203.233, 133.484)), (' C 673  SER  OG ', ' C 674  TYR  N  ', -0.434, (218.962, 204.478, 208.25)), (' B 332  ILE HG12', ' B 362  VAL HG23', -0.433, (185.327, 224.585, 152.307)), (' A 162  SER  OG ', ' A 163  ALA  N  ', -0.432, (198.947, 142.699, 137.493)), (' C 726  ILE HG13', ' C1061  VAL HG22', -0.432, (192.12, 205.462, 217.037)), (' B  54  LEU  HB2', ' B 195  LYS  HZ3', -0.43, (152.408, 192.159, 168.692)), (' A1141  LEU HD12', ' A1144  GLU  HB2', -0.43, (188.741, 179.917, 273.68)), (' C 228  ASP  N  ', ' C 228  ASP  OD1', -0.429, (202.81, 222.903, 160.436)), (' B  92  PHE  O  ', ' B 192  PHE  N  ', -0.428, (138.517, 190.047, 169.502)), (' B 472  ILE HD13', ' B 484  GLU  HG2', -0.426, (223.592, 198.243, 131.187)), (' C 105  ILE HG22', ' C 118  LEU HD22', -0.426, (220.625, 224.028, 152.124)), (' C 676  THR  OG1', ' C 690  GLN  OE1', -0.425, (225.64, 211.153, 208.984)), (' C 273  ARG  HA ', ' C 273  ARG  HD3', -0.424, (214.212, 206.942, 176.031)), (' C 359  SER  OG ', ' C 360  ASN  OD1', -0.424, (214.591, 163.148, 150.773)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.423, (193.806, 206.193, 230.883)), (' A 985  ASP  N  ', ' A 985  ASP  OD2', -0.422, (202.168, 186.75, 158.519)), (' C 969  ASN  N  ', ' C 969  ASN  OD1', -0.422, (192.643, 200.462, 173.511)), (' B 723  THR  OG1', ' B 724  THR  N  ', -0.42, (167.308, 185.768, 223.746)), (' B 104  TRP  HA ', ' B 240  THR  HA ', -0.418, (134.17, 194.449, 159.08)), (' C 981  LEU  HA ', ' C 981  LEU HD23', -0.418, (179.71, 203.122, 164.845)), (' A 413  GLY  O  ', ' A 414  GLN  NE2', -0.417, (178.584, 195.191, 151.99)), (' B1086  LYS  HA ', ' B1086  LYS  HD3', -0.417, (193.305, 203.661, 262.46)), (' C  37  TYR  OH ', ' C 195  LYS  NZ ', -0.416, (208.915, 215.687, 169.878)), (' B 417  LYS  O  ', ' B 422  ASN  ND2', -0.415, (206.768, 195.648, 141.485)), (' B 532  ASN  N  ', ' B 532  ASN  OD1', -0.415, (172.897, 228.021, 165.393)), (' C 119  ILE  HA ', ' C 128  ILE HD12', -0.414, (214.569, 226.393, 154.971)), (' C 433  VAL HG12', ' C 512  VAL HG22', -0.413, (195.829, 173.049, 145.412)), (' C 310  LYS  NZ ', ' C 663  ASP  OD1', -0.413, (212.326, 204.486, 209.08)), (' B 201  PHE  HB3', ' B 229  LEU  HB2', -0.412, (146.745, 186.485, 157.159)), (' C 531  THR HG22', ' C 532  ASN  H  ', -0.411, (228.669, 180.002, 163.052)), (' A 490  PHE  HA ', ' A 491  PRO  HD3', -0.411, (162.844, 210.738, 135.382)), (' C 236  THR HG22', ' C 237  ARG  HG2', -0.411, (224.128, 211.899, 156.518)), (' C 627  ASP  N  ', ' C 627  ASP  OD1', -0.411, (227.877, 198.813, 179.669)), (' C 947  LYS  HB3', ' C 947  LYS  HE2', -0.411, (193.95, 199.997, 210.736)), (' C 777  ASN  OD1', ' C1019  ARG  NH1', -0.41, (179.389, 194.9, 209.934)), (' A 212  LEU HD21', ' A 215  ASP  HB3', -0.41, (201.855, 133.072, 177.038)), (' B 574  ASP  HA ', ' B 587  ILE  HB ', -0.41, (183.738, 218.665, 178.116)), (' B 900  MET  HB3', ' B 900  MET  HE2', -0.409, (174.805, 171.733, 245.453)), (' A 726  ILE HG12', ' A1061  VAL HG22', -0.409, (201.83, 172.121, 216.615)), (' A 560  LEU  HA ', ' A 560  LEU HD23', -0.409, (146.222, 171.619, 174.08)), (' A 319  ARG  H  ', ' A 319  ARG  HG2', -0.404, (182.158, 156.773, 180.801)), (' A 947  LYS  HB3', ' A 947  LYS  HE2', -0.404, (195.264, 173.615, 210.331)), (' C 862  PRO  HA ', ' C 863  PRO  HD3', -0.403, (177.148, 208.977, 202.666)), (' B 328  ARG  NH2', ' B 578  ASP  OD1', -0.403, (180.684, 228.752, 166.923)), (' B 105  ILE HG23', ' B 241  LEU HD11', -0.403, (133.991, 193.967, 154.85)), (' C 305  SER  OG ', ' C 306  PHE  N  ', -0.402, (205.434, 211.922, 193.35)), (' A 426  PRO  HG2', ' A 429  PHE  HB2', -0.402, (168.976, 189.616, 155.151)), (' A 125  ASN  ND2', ' A 172  SER  O  ', -0.402, (214.724, 146.217, 150.175)), (' A 141  LEU  O  ', ' A 244  LEU  N  ', -0.402, (205.011, 129.556, 150.563)), (' A 659  SER  HB3', ' A 698  SER  HB3', -0.402, (178.009, 152.844, 215.81)), (' A 526  GLY  HA3', ' A 527  PRO  HD3', -0.4, (165.335, 167.749, 150.147)), (' B 439  ASN HD21', ' B 506  GLN  HG2', -0.4, (191.366, 196.08, 127.653)), (' A 528  LYS  HA ', ' A 528  LYS  HD3', -0.4, (167.565, 161.944, 153.717)), (' B 914  ASN  N  ', ' B 914  ASN  OD1', -0.4, (172.331, 183.372, 250.313))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
