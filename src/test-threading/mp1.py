from multiprocessing import Process, Pipe


def f(child_conn):
  msg="mp1 is sending this to a child connection"
  child_conn.send(msg)
  child_conn.close()