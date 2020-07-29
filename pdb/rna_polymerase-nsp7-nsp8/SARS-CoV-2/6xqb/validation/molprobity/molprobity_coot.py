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
data['omega'] = [('A', ' 216 ', 'TRP', None, (121.635, 104.436, 69.33800000000001)), ('A', ' 235 ', 'ASP', None, (105.044, 105.824, 71.201)), ('A', ' 466 ', 'ILE', None, (99.849, 102.385, 80.407)), ('A', ' 609 ', 'VAL', None, (82.719, 75.497, 78.38100000000003)), ('A', ' 706 ', 'ALA', None, (99.513, 86.87500000000003, 77.996)), ('A', ' 755 ', 'MET', None, (84.14399999999999, 82.09700000000002, 84.27200000000003)), ('B', ' 181 ', 'ALA', None, (116.78900000000003, 96.951, 128.165))]
data['rota'] = [('A', ' 463 ', 'MET', 0.277448522830967, (103.341, 103.134, 86.071)), ('A', ' 703 ', 'ASN', 0.17620870306790218, (94.77700000000002, 87.20900000000002, 78.86))]
data['cbeta'] = []
data['probe'] = [(' A 531  THR  OG1', ' A 654  ARG  NH2', -0.873, (82.028, 115.65, 98.256)), (' A 207  LEU HD12', ' A 240  LEU HD13', -0.84, (110.604, 99.712, 73.596)), (' B  83  VAL HG22', ' B  87  MET  HE2', -0.839, (82.055, 114.956, 117.416)), (' A 556  THR  OG1', ' A 624  ARG  NH2', -0.819, (98.28, 95.635, 108.013)), (' A 623  ASP  OD2', ' A 624  ARG  NH1', -0.79, (97.415, 95.416, 104.49)), (' A 427  GLY  O  ', ' A 430  LYS  NZ ', -0.788, (89.554, 58.687, 116.434)), (' A 676  LYS  NZ ', ' A 679  GLY  O  ', -0.783, (96.975, 102.012, 101.502)), (' A 795  SER  OG ', ' A 798  LYS  NZ ', -0.783, (103.059, 80.932, 96.412)), (' A 840  ALA  O  ', ' A 858  ARG  NH1', -0.773, (86.334, 78.17, 117.933)), (' A 810  HIS  O  ', ' A 816  HIS  ND1', -0.75, (89.636, 72.118, 98.208)), (' A 323  PRO  O  ', ' B 118  ASN  ND2', -0.736, (106.059, 116.202, 102.841)), (' A 283  PHE  O  ', ' A 287  PHE  N  ', -0.731, (109.249, 114.256, 78.126)), (' B 171  GLU  OE2', ' B 176  ASN  ND2', -0.726, (124.992, 98.103, 132.559)), (' A 457  ARG  NH2', ' A 458  TYR  OH ', -0.725, (110.206, 93.319, 105.082)), (' A 503  GLY  O  ', ' A 507  ASN  N  ', -0.719, (87.279, 108.084, 115.866)), (' A 822  GLN  NE2', ' A 916  TRP  O  ', -0.715, (70.589, 68.463, 96.663)), (' A 759  SER  HG ', " E   9    A HO2'", -0.713, (88.738, 89.979, 99.145)), (' A 785  VAL  O  ', ' A 789  GLN  N  ', -0.709, (104.019, 92.529, 87.537)), (' A 312  ASN  ND2', ' A 463  MET  SD ', -0.707, (100.827, 104.453, 83.311)), (' A 623  ASP  OD1', ' A 680  THR  OG1', -0.704, (94.469, 95.866, 101.463)), (' A 636  LEU HD21', ' A 655  LEU HD22', -0.703, (89.905, 109.149, 88.498)), (' A 588  VAL HG11', ' A 756  MET  HE2', -0.686, (80.921, 82.145, 92.07)), (' A 326  PHE  O  ', ' B 118  ASN  ND2', -0.676, (104.898, 117.117, 102.201)), (' A 483  TYR  O  ', ' A 641  LYS  NZ ', -0.675, (76.103, 99.576, 84.285)), (' A  31  VAL  N  ', ' A  50  LYS  O  ', -0.674, (120.574, 83.569, 66.903)), (' A 700  VAL  O  ', ' A 704  VAL HG23', -0.661, (94.821, 90.496, 78.664)), (' A 211  ASP  OD2', ' A 213  ASN  ND2', -0.658, (125.998, 99.51, 73.276)), (' A 611  ASN  ND2', ' A 769  THR  OG1', -0.653, (91.105, 72.493, 72.913)), (' A 473  VAL  HA ', ' A 476  VAL HG12', -0.642, (87.051, 98.221, 82.124)), (' A 403  ASN  ND2', ' B 129  MET  SD ', -0.642, (107.463, 113.396, 123.557)), (' A 598  TRP  HA ', ' A 601  MET  HE3', -0.641, (77.953, 77.465, 93.606)), (' A 472  VAL HG22', ' A 700  VAL HG11', -0.64, (91.882, 93.741, 79.433)), (' B 101  ASP  O  ', ' B 105  ASN  ND2', -0.638, (107.277, 134.838, 115.042)), (' A 501  SER  N  ', ' F   1    G  OP1', -0.638, (84.158, 100.936, 115.101)), (' A 348  PHE  CZ ', ' A 660  ALA  HB2', -0.637, (93.996, 113.682, 98.619)), (' A 632  ILE HG23', ' A 655  LEU HD11', -0.636, (91.73, 107.839, 91.22)), (' A 579  ILE  CG2', ' A 587  VAL HG21', -0.635, (78.747, 90.808, 90.598)), (' A 241  LEU HD12', ' A 244  ILE HD11', -0.632, (111.309, 99.455, 80.959)), (' A 469  LEU HD11', ' A 633  MET  HG2', -0.632, (93.319, 100.804, 86.278)), (' B 167  VAL HG21', ' B 172  ILE HD11', -0.631, (119.641, 105.059, 128.281)), (' A 332  LYS  O  ', ' A 333  ILE HD13', -0.629, (94.178, 131.237, 106.826)), (' A 500  LYS  NZ ', ' F   2    U  OP2', -0.625, (82.283, 96.956, 111.406)), (' A 515  TYR  HB3', ' A 566  MET  HE1', -0.625, (78.541, 110.509, 110.468)), (' A 136  GLU  N  ', ' A 136  GLU  OE1', -0.621, (109.175, 81.321, 87.088)), (' C  27  LYS  O  ', ' C  31  GLN  NE2', -0.619, (113.716, 87.077, 126.656)), (' B 161  ASP  O  ', ' B 181  ALA  HB3', -0.618, (114.249, 99.271, 127.323)), (' A 704  VAL  O  ', ' A 708  LEU  N  ', -0.606, (99.323, 88.392, 74.724)), (' A 295  HIS  N  ', ' A 310  CYS  SG ', -0.606, (97.821, 115.999, 81.59)), (' A 459  ASN  OD1', ' A 460  LEU  N  ', -0.602, (104.706, 100.5, 96.589)), (' A 297  ASN  OD1', ' A 353  VAL HG12', -0.602, (98.611, 121.492, 90.352)), (' A 578  SER  O  ', ' A 582  THR  OG1', -0.602, (73.134, 92.526, 89.533)), (' B 162  ALA  HB2', ' B 183  PRO  HB2', -0.6, (113.104, 100.129, 123.293)), (' A 692  SER  O  ', ' A 696  ILE HD12', -0.598, (88.116, 92.014, 89.459)), (' A  46  ALA  HB2', ' A 709  SER  HA ', -0.597, (105.652, 87.525, 72.515)), (' B 159  VAL HG22', ' B 186  VAL HG13', -0.594, (118.249, 110.088, 125.19)), (' A 704  VAL HG13', ' A 727  LEU HD21', -0.588, (96.893, 92.136, 74.191)), (' C  10  SER  HB3', ' C  39  ILE HD13', -0.586, (104.054, 73.397, 124.273)), (' A 631  ARG  NH1', ' A 635  SER  OG ', -0.584, (89.077, 102.964, 94.556)), (' C  36  HIS  CE1', ' C  40  LEU HD11', -0.579, (101.325, 77.668, 120.322)), (' A 723  LEU HD13', ' A 744  GLU  HG2', -0.578, (87.464, 89.035, 68.966)), (' A 778  SER  OG ', ' A 780  LYS  NZ ', -0.576, (100.336, 80.049, 80.82)), (' A 146  LEU HD22', ' A 174  VAL HG12', -0.575, (119.548, 93.436, 89.68)), (' A 908  THR HG23', ' A 910  ASP  H  ', -0.574, (67.875, 66.03, 111.86)), (' A 389  LEU HD23', ' B 130  VAL HG22', -0.572, (115.849, 110.681, 116.148)), (' B 134  ASP  OD1', ' B 137  THR  OG1', -0.57, (120.903, 101.556, 118.116)), (' A 207  LEU HD21', ' A 237  TYR  CE1', -0.564, (113.351, 102.801, 73.936)), (' A 856  ILE HD13', ' A 891  LEU HD23', -0.564, (74.844, 74.01, 122.759)), (' A 234  VAL  O  ', ' A 237  TYR  N  ', -0.562, (107.1, 103.459, 72.419)), (' B 161  ASP  HA ', ' B 184  LEU HD23', -0.56, (116.495, 102.471, 126.243)), (' A 134  PHE  O  ', ' A 784  SER  OG ', -0.559, (107.021, 85.076, 84.804)), (' A 705  ASN  ND2', ' A 708  LEU HD12', -0.558, (101.297, 91.89, 76.407)), (' D  84  THR  O  ', ' D  88  GLN  NE2', -0.557, (94.292, 79.497, 137.096)), (' A 169  PRO  O  ', ' A 172  LEU HD13', -0.552, (114.053, 96.025, 98.769)), (' A 483  TYR  HE1', ' A 582  THR HG21', -0.549, (74.236, 91.63, 87.235)), (' A 120  THR  OG1', ' A 211  ASP  OD1', -0.549, (124.064, 96.895, 73.511)), (' A 687  THR  O  ', ' A 691  ASN  ND2', -0.548, (88.764, 94.745, 97.724)), (' A 241  LEU  CD1', ' A 244  ILE HD11', -0.54, (111.84, 99.729, 80.374)), (' A 388  LEU  HB2', ' A 400  ALA  HB2', -0.538, (106.112, 112.05, 118.508)), (' A 608  ASP  OD2', ' A 751  LYS  NZ ', -0.537, (79.59, 76.457, 73.573)), (' C  12  VAL  O  ', ' C  15  SER  OG ', -0.537, (97.653, 78.907, 130.066)), (' A 876  GLU  O  ', ' A 880  VAL HG23', -0.536, (85.563, 62.976, 110.491)), (' C  36  HIS  HE1', ' C  40  LEU HD11', -0.534, (100.63, 78.01, 120.87)), (' A 477  ASP  OD1', ' A 478  LYS  N  ', -0.53, (82.357, 96.92, 79.002)), (' A 516  TYR  CD1', ' A 566  MET  HE2', -0.528, (77.412, 107.597, 108.35)), (' A 628  ASN  ND2', ' A 677  PRO  O  ', -0.527, (101.179, 104.359, 97.193)), (' A 152  CYS  HB2', ' A 174  VAL HG13', -0.526, (121.44, 92.791, 91.63)), (' A 278  GLU  N  ', ' A 278  GLU  OE1', -0.525, (108.944, 123.031, 87.862)), (' C  19  GLN  NE2', ' D  84  THR  OG1', -0.525, (94.032, 82.263, 133.573)), (' C   5  ASP  OD1', ' C   6  VAL  N  ', -0.525, (100.445, 66.753, 124.372)), (' A 410  VAL HG11', ' A 443  ALA  HA ', -0.523, (98.668, 86.542, 120.489)), (' A 531  THR  O  ', ' A 657  ASN  ND2', -0.52, (85.544, 115.316, 96.943)), (' A 160  LYS  NZ ', ' A 167  GLU  OE2', -0.519, (113.64, 84.344, 104.209)), (' A 629  MET  HA ', ' A 632  ILE HD12', -0.518, (96.768, 105.079, 90.325)), (' A 241  LEU  O  ', ' A 245  LEU HD21', -0.517, (110.173, 102.978, 81.106)), (' A 786  LEU  O  ', ' A 791  ASN  N  ', -0.517, (104.788, 92.305, 91.948)), (' A 388  LEU HD22', ' A 400  ALA  HB2', -0.516, (105.684, 110.55, 118.649)), (' A 630  LEU HD22', ' A 694  PHE  HE1', -0.516, (96.426, 95.989, 90.495)), (' A 796  GLU  N  ', ' A 796  GLU  OE1', -0.513, (103.688, 78.288, 91.941)), (' A 387  LEU HD12', ' A 388  LEU  H  ', -0.51, (108.541, 114.373, 115.717)), (' C  22  VAL HG13', ' C  28  LEU HD23', -0.506, (108.903, 88.1, 132.025)), (' A 750  ARG  O  ', ' A 754  SER  OG ', -0.504, (82.814, 81.316, 79.176)), (' A 454  ASP  OD1', ' A 455  TYR  N  ', -0.502, (106.775, 95.549, 108.098)), (' A 185  ALA  HB1', ' A 210  GLN  NE2', -0.502, (117.288, 104.355, 75.35)), (' A 249  ARG  O  ', ' A 252  THR HG23', -0.502, (115.866, 106.493, 90.941)), (' A 210  GLN  NE2', ' A 214  GLY  O  ', -0.5, (118.536, 104.477, 73.597)), (' A 428  PHE  CE2', ' A 883  LEU HD22', -0.499, (84.766, 63.631, 117.282)), (' D 101  ASP  OD1', ' D 102  ALA  N  ', -0.497, (111.633, 62.981, 132.217)), (' A 625  ALA  HB1', ' A 790  ASN  O  ', -0.496, (102.911, 94.32, 95.208)), (' B 142  CYS  SG ', ' B 186  VAL HG11', -0.496, (119.229, 110.43, 122.478)), (' B 104  ASN  ND2', ' B 107  ILE HD11', -0.495, (102.029, 136.413, 109.792)), (' A 477  ASP  O  ', ' A 481  ASP  N  ', -0.495, (79.294, 97.683, 81.488)), (' A 211  ASP  OD1', ' A 212  LEU  N  ', -0.495, (122.491, 98.275, 74.58)), (' A 560  VAL HG12', ' A 561  SER  H  ', -0.494, (88.858, 107.703, 107.73)), (' A 837  ILE HG23', ' A 862  LEU  HB3', -0.493, (83.039, 73.923, 113.615)), (' A 740  ASP  OD1', ' A 741  PHE  N  ', -0.493, (85.403, 96.113, 68.214)), (' A 689  TYR  OH ', " F   3    G  O2'", -0.493, (79.392, 93.378, 98.906)), (' A 576  LEU  O  ', ' A 580  ALA  N  ', -0.491, (75.681, 93.814, 93.688)), (' C  19  GLN  NE2', ' D  87  MET  SD ', -0.491, (94.84, 81.654, 132.408)), (' C  13  LEU HD23', ' C  55  LEU HD23', -0.49, (105.198, 75.558, 128.394)), (' A 590  GLY  N  ', " F   4    G  O2'", -0.488, (77.08, 87.665, 98.477)), (' A 233  VAL HG12', ' A 235  ASP  H  ', -0.488, (104.464, 106.104, 70.0)), (' A 848  VAL HG22', ' A 855  MET  HB3', -0.487, (79.784, 78.87, 123.116)), (' A 241  LEU HD12', ' A 244  ILE  CD1', -0.483, (111.733, 99.309, 81.457)), (' A 908  THR HG23', ' A 910  ASP  N  ', -0.483, (67.845, 66.09, 111.355)), (' A 720  VAL  CG2', ' A 775  LEU HD21', -0.482, (93.161, 81.826, 69.63)), (' A 190  VAL HG21', ' A 285  ARG  O  ', -0.481, (112.505, 114.12, 76.985)), (' A 304  ASP  OD1', ' A 305  ARG  N  ', -0.479, (88.001, 108.991, 82.011)), (' A 305  ARG  HE ', ' A 735  ARG HH12', -0.478, (89.629, 107.043, 76.467)), (' A 749  LEU HD23', ' A 750  ARG  N  ', -0.477, (84.114, 85.38, 78.282)), (' A 814  SER  O  ', ' A 815  GLN  NE2', -0.477, (85.37, 75.744, 103.474)), (' A 494  ILE  O  ', ' A 494  ILE HG22', -0.477, (71.693, 98.067, 102.961)), (' A 348  PHE  HZ ', ' A 660  ALA  HB2', -0.476, (93.629, 113.884, 98.706)), (' B  95  LEU  HA ', ' B  98  LEU HD12', -0.476, (96.16, 126.742, 119.727)), (' A 332  LYS  HA ', ' A 341  VAL HG22', -0.475, (96.935, 129.519, 109.73)), (' A 783  LYS  NZ ', ' A 796  GLU  OE1', -0.475, (105.58, 78.931, 90.308)), (' A 257  VAL HG22', ' A 266  ILE HG12', -0.474, (120.743, 120.96, 94.448)), (' A 146  LEU HD22', ' A 174  VAL  CG1', -0.473, (120.279, 93.231, 90.371)), (' C  52  MET  O  ', ' C  56  LEU HD13', -0.473, (108.985, 73.261, 129.933)), (' A 498  LEU  H  ', ' A 498  LEU HD23', -0.472, (74.55, 99.004, 112.417)), (' A 119  LEU  H  ', ' A 119  LEU HD23', -0.469, (128.309, 96.005, 69.124)), (' A 470  LEU  O  ', ' A 473  VAL HG12', -0.469, (90.392, 101.289, 79.543)), (' A 704  VAL  O  ', ' A 707  LEU  N  ', -0.469, (98.751, 87.709, 75.347)), (' A 820  VAL HG21', ' A 829  LEU HD12', -0.467, (77.488, 65.293, 98.089)), (' A 514  LEU  O  ', ' A 518  SER  N  ', -0.466, (73.638, 110.859, 113.825)), (' A 234  VAL  O  ', ' A 236  SER  N  ', -0.465, (106.139, 104.062, 71.636)), (' A 387  LEU HD21', ' B 128  LEU HD13', -0.459, (112.915, 116.506, 116.295)), (' A 270  LEU  C  ', ' A 271  LEU HD12', -0.457, (109.781, 125.554, 104.048)), (' A 450  ILE  H  ', ' A 450  ILE HD12', -0.457, (105.061, 98.06, 116.125)), (' A 684  ASP  OD1', ' A 685  ALA  N  ', -0.456, (85.77, 101.517, 101.921)), (' A 241  LEU  HG ', ' A 245  LEU HD21', -0.456, (111.153, 102.984, 81.206)), (' A 375  ALA  O  ', ' A 381  HIS  NE2', -0.454, (91.334, 116.801, 114.601)), (' A 720  VAL HG21', ' A 775  LEU HD21', -0.454, (93.167, 81.401, 69.691)), (' A 875  GLN  O  ', ' A 878  ALA  HB3', -0.451, (83.154, 58.787, 109.034)), (' A 825  ASP  OD1', ' A 826  TYR  N  ', -0.45, (73.85, 62.773, 88.436)), (' A 468  GLN  N  ', ' A 468  GLN  OE1', -0.449, (98.045, 99.731, 77.827)), (' A 315  VAL HG23', ' A 316  LEU  N  ', -0.449, (105.096, 108.41, 87.879)), (' A 630  LEU HD22', ' A 694  PHE  CE1', -0.449, (96.192, 95.667, 90.88)), (' A 620  PRO  HG2', ' A 792  VAL HG11', -0.448, (102.392, 87.398, 96.835)), (' A 781  ASN  O  ', ' A 785  VAL HG23', -0.447, (102.266, 87.637, 84.661)), (' A 120  THR  OG1', ' A 122  TYR  O  ', -0.447, (123.025, 94.915, 74.299)), (' A 414  ASN  ND2', ' A 846  ASP  OD1', -0.446, (88.83, 82.989, 126.86)), (' A 293  THR HG21', ' A 302  LEU HD23', -0.446, (94.504, 115.183, 77.986)), (' A 469  LEU  O  ', ' A 469  LEU HD23', -0.446, (92.143, 100.761, 82.383)), (' C   7  LYS  HE3', ' C  42  ALA  HB3', -0.445, (104.478, 69.616, 117.97)), (' B 176  ASN  OD1', ' B 179  ASN  ND2', -0.444, (124.301, 94.82, 132.097)), (' A 609  VAL HG21', ' A 765  CYS  HB3', -0.444, (85.025, 76.948, 82.109)), (' A  33  ARG  HB2', ' A  35  PHE  CE2', -0.443, (116.311, 88.969, 68.306)), (' A 307  ILE HG21', ' A 655  LEU  CD2', -0.443, (91.25, 110.581, 88.903)), (' A 283  PHE  O  ', ' A 286  TYR  N  ', -0.441, (110.185, 114.798, 79.056)), (' A 472  VAL HG22', ' A 700  VAL  CG1', -0.441, (92.592, 93.369, 80.107)), (' A 516  TYR  CE1', ' A 566  MET  HE2', -0.44, (78.008, 107.751, 108.539)), (' A 768  SER  O  ', ' A 772  SER  N  ', -0.438, (96.12, 75.359, 76.72)), (' A 564  SER  HG ', ' A 661  GLN  CD ', -0.438, (86.993, 109.551, 102.286)), (' A 878  ALA  O  ', ' A 881  PHE  N  ', -0.438, (81.076, 63.375, 111.189)), (' A 579  ILE HG22', ' A 587  VAL HG21', -0.438, (78.239, 91.036, 91.558)), (' A 753  PHE  CE1', ' A 777  ALA  HB3', -0.436, (92.499, 81.846, 82.294)), (' A 270  LEU  O  ', ' A 271  LEU HD12', -0.436, (109.464, 125.223, 104.723)), (' A 307  ILE HG21', ' A 655  LEU HD23', -0.435, (91.237, 111.011, 89.0)), (' A 572  HIS  CE1', ' A 638  LEU HD23', -0.435, (83.574, 103.166, 93.683)), (' C  23  GLU  N  ', ' C  23  GLU  OE1', -0.434, (104.189, 90.473, 130.744)), (' A 348  PHE  CE1', ' A 660  ALA  HB2', -0.433, (94.339, 113.268, 99.179)), (' A 280  LEU  O  ', ' A 280  LEU HD13', -0.432, (107.855, 120.467, 80.858)), (' A 704  VAL HG13', ' A 727  LEU  CD2', -0.431, (96.64, 92.127, 74.19)), (' A 560  VAL HG12', ' A 561  SER  N  ', -0.431, (88.728, 107.461, 108.233)), (' A 609  VAL HG21', ' A 765  CYS  SG ', -0.431, (84.936, 76.228, 81.809)), (' A 135  ASP  O  ', ' A 138  ASN  N  ', -0.43, (112.677, 80.923, 84.815)), (' A 698  GLN HE21', ' A 786  LEU HD11', -0.428, (98.339, 90.148, 89.226)), (' A 297  ASN  CG ', ' A 353  VAL HG12', -0.427, (98.722, 121.65, 89.767)), (' B 159  VAL HG13', ' B 186  VAL HG22', -0.427, (117.82, 107.911, 125.296)), (' A 540  THR  N  ', ' A 665  GLU  OE1', -0.427, (94.644, 108.22, 108.618)), (' A 128  VAL HG13', ' A 244  ILE HD13', -0.425, (110.495, 96.578, 80.855)), (' A 480  PHE  O  ', ' A 641  LYS  NZ ', -0.425, (76.902, 99.184, 84.365)), (' A 488  ILE HD11', ' A 493  VAL HG22', -0.424, (73.279, 104.755, 99.171)), (' B 167  VAL  CG2', ' B 172  ILE HD11', -0.422, (120.164, 105.16, 128.896)), (' A 332  LYS  C  ', ' A 333  ILE HD13', -0.422, (94.447, 131.093, 107.861)), (' A 572  HIS  CD2', ' A 638  LEU HD23', -0.422, (83.413, 103.05, 94.529)), (' A 405  VAL HG21', ' B 131  VAL HG21', -0.422, (109.613, 106.263, 121.023)), (' A 233  VAL HG11', ' A 733  ARG HH21', -0.421, (102.691, 105.622, 67.603)), (' A 390  ASP  HB2', ' A 392  ARG  HE ', -0.421, (110.285, 103.534, 116.93)), (' A 606  TYR  CD2', ' A 805  LEU HD23', -0.418, (82.316, 71.752, 84.277)), (' A 628  ASN  HB3', ' A 663  LEU HD11', -0.417, (97.302, 104.524, 95.518)), (' A 207  LEU HD21', ' A 237  TYR  HE1', -0.417, (114.134, 102.666, 74.127)), (' A 527  LEU HD23', ' A 531  THR  CG2', -0.417, (82.569, 115.818, 101.983)), (' B 132  ILE HD11', ' B 184  LEU  HG ', -0.416, (118.491, 102.701, 123.567)), (' A 494  ILE HD12', ' A 577  LYS  HG3', -0.416, (72.061, 98.529, 97.741)), (' A 132  ARG  HA ', ' A 788  TYR  CD1', -0.416, (107.485, 91.076, 83.594)), (' A 819  LEU HD11', ' A 826  TYR  HB3', -0.413, (77.979, 62.95, 90.215)), (' A 853  THR  OG1', ' A 854  LEU  N  ', -0.413, (74.097, 81.963, 124.554)), (' A 376  ALA  HB2', ' A 506  PHE  HE2', -0.411, (87.089, 113.655, 112.371)), (' A 792  VAL HG12', ' A 793  PHE  N  ', -0.41, (104.722, 87.648, 95.518)), (' C   5  ASP  OD2', ' D  97  LYS  NZ ', -0.407, (98.639, 63.022, 126.132)), (" F   1    G  O2'", " F   2    U  O4'", -0.407, (84.207, 98.597, 107.324)), (' A 483  TYR  CD2', ' A 579  ILE HD11', -0.407, (77.839, 94.793, 87.761)), (' A 471  PHE  O  ', ' A 475  VAL HG23', -0.407, (89.396, 96.832, 77.609)), (' A 609  VAL HG11', ' A 766  PHE  N  ', -0.407, (87.45, 76.187, 81.333)), (' A 588  VAL HG22', ' A 757  ILE  O  ', -0.406, (82.564, 85.583, 93.165)), (' A 460  LEU HD23', ' A 461  PRO  O  ', -0.406, (106.838, 101.792, 92.323)), (' A 606  TYR  O  ', ' A 609  VAL HG23', -0.404, (82.625, 76.637, 80.485)), (' B 132  ILE  O  ', ' B 183  PRO  HA ', -0.403, (115.879, 101.192, 121.337)), (' A 303  ASP  HA ', ' A 648  LEU HD11', -0.402, (86.968, 114.145, 81.681)), (' A 748  TYR  OH ', ' A 775  LEU HD23', -0.402, (91.941, 82.336, 72.099)), (' A 602  LEU  HA ', ' A 605  VAL HG12', -0.402, (80.657, 76.388, 87.592)), (' A 874  ASN  HB3', ' A 877  TYR  CD2', -0.401, (87.395, 60.592, 105.07)), (' A 460  LEU HD23', ' A 461  PRO  N  ', -0.401, (106.816, 101.992, 93.366)), (' A 257  VAL HG22', ' A 266  ILE  CG1', -0.401, (120.394, 120.297, 94.366)), (' A 819  LEU HD12', ' A 827  VAL  O  ', -0.4, (78.576, 65.03, 92.262)), (' A 416  ASN  OD1', ' A 844  VAL HG23', -0.4, (86.444, 76.816, 122.523))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
