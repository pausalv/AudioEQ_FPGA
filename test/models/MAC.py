from cocotb.triggers import RisingEdge
import cocotb

class MAC:
  Win = 0
  Wc = 0
  Wout = 0

  ic_ce = 0
  ic_rst = 0
  ic_neg_acc = 0

  id_din = 0
  id_coef = 0

  od_dout = 0

  acc = 0

  def __init__(self, Win, Wc, Wout, id_din = 0, id_coef = 0, ic_ce = 0, ic_rst = 0, ic_neg_acc = 0):
    self.Win = Win
    self.Wc = Wc
    self.Wout = Wout
    self.id_din = id_din
    self.id_coef = id_coef
    self.ic_ce = ic_ce
    self.ic_rst = ic_rst
    self.ic_neg_acc = ic_neg_acc

  def set_ce(self, ce):
    self.ic_ce = ce

  def set_rst(self, rst):
    self.ic_rst = rst
  
  def set_neg_acc(self, neg_acc):
    self.ic_neg_acc = neg_acc
  
  def set_din(self, din):
    self.id_din = din

  def set_coef(self, coef):
    self.id_coef = coef
  
  def get_dout(self):
    if self.ic_rst == 1:
      self.acc = 0
    elif self.ic_ce == 1:
        if self.ic_neg_acc == 1:
          self.acc = self.acc - self.id_din * self.id_coef
        else:
          self.acc = self.acc + self.id_din * self.id_coef
    return self.acc
  