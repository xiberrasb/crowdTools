import pymel.core as pm

class CrowdUtils() :
	def getjoints(self) :
		pm.select('RIG:RIG')
		jointslist = pm.listRelatives(type='joint', ad=True)
		pm.select(cl=True)
		return jointslist

	def attrcheck(self, *args) :
		jointslist = self.getjoints()
		mflagged = []
		i = 0
		while i < len(args) :
			for mjoint in jointslist :
				try :
					mjoint.attr(args[i]) is not None
					mflagged.append(mjoint)
				except AttributeError :
					pass
			i += 1
		return mflagged

	def deletecrowdrig(self) :
		try :
			pm.ls('crowdRig') is not None
			pm.delete('crowdRig')
			print 'crowdRig deleted'
		except pm.MayaObjectError :
			print 'No crowdRig node to delete'
			pass

	def checkcrowdriglen(self) :
		pm.select('crowdRig')
		jntlist = pm.listRelatives(typ='joint')
		print len(jntlist)

	def getjointorients(self, mjoint) :
		jox = mjoint.jointOrientX.get()
		joy = mjoint.jointOrientY.get()
		joz = mjoint.jointOrientZ.get()
		return jox, joy, joz

	def setjointorients(self, newjoint, jox, joy, joz) :
		newjoint.jointOrientX.set(jox)
		newjoint.jointOrientY.set(joy)
		newjoint.jointOrientZ.set(joz)

	def getjointrot(self, mjoint) :
		rox = mjoint.rx.get()
		roy = mjoint.ry.get()
		roz = mjoint.rz.get()
		return rox, roy, roz

	def setjointrot(self, newjoint, rox, roy, roz) :
		newjoint.rx.set(rox)
		newjoint.ry.set(roy)
		newjoint.rz.set(roz)

	def getjointscale(self, mjoint) :
		sox = mjoint.sx.get()
		soy = mjoint.sy.get()
		soz = mjoint.sz.get()
		return sox, soy, soz

	def getnamespace(self) :
		mscene = pm.ls(s=False, typ='mesh')
		if mscene is not None :
			for mobj in mscene :
				return mobj.namespace()
		else :
			pass

	def removedigits(self, sel, digits) :
		sel = pm.ls(sl=True)
		i = 0
		while i < len(sel) :
			for i, nodes in enumerate(sel) :
				sel[i].rename(sel[i].name().replace(digits, ''))
			i += 1

	def getskindatas(self) :
		selection = pm.ls(sl=True)
		meshidx = 0
		for meshidx, elem in enumerate(selection) :
			elem = selection[meshidx].getShape()
			scluster = pm.listConnections(elem, t='skinCluster')
			skin = pm.skinCluster(scluster, inf=elem, q=True, wi=True)
			idx = 0
			while idx < len(elem.vtx) :
				spercent = pm.skinPercent(scluster[0], elem.vtx[idx], q=True, v=True, r=True)
				idx += 1

	def createcrowdrig(self, *args) :
		jointtransform = []
		if pm.ls('crowdRig', an=True) :
			print 'crowdRig group already exists'
			self.deletecrowdrig()
			self.createcrowdrig()
			pass
		else :
			mgroup = pm.group(n='crowdRig', w=True)
			pm.select(cl=True)
			mflagged = self.attrcheck('Right_arm_GolaemFLAG', 'Left_arm_GolaemFLAG', 'Right_leg_GolaemFLAG',
									  'Left_leg_GolaemFLAG', 'Hips_GolaemFLAG', 'Head_GolaemFLAG', 'Spine_GolaemFLAG')
			for i, mjoint in enumerate(mflagged) :
				jointcrowd = mjoint.name() + '_CROWDRIG'
				newjoint = pm.joint(n=jointcrowd, rad=0.097)
				newjoint.segmentScaleCompensate.set(0)
				if self.getjointscale(mjoint) == (1, 1, 1) :
					pm.parent(newjoint, mjoint)
					newjoint.translate.set(0, 0, 0)
					newjoint.jointOrient.set(0, 0, 0)
				else :
					pm.parent(newjoint, mjoint)
					jointtransform = newjoint.listRelatives(p=True)
					pm.parent(newjoint, jointtransform[0])
					jointtransform[0].translate.set(0, 0, 0)
					jointtransform[0].rotate.set(0, 0, 0)
					newjoint.translate.set(0, 0, 0)
					newjoint.jointOrient.set(0, 0, 0)
				pm.parent(newjoint, mgroup)
				pm.rename(newjoint, mjoint)
				self.removedigits(newjoint, '_orig')
			pm.delete(jointtransform)
			headctrljnt = pm.duplicate('crowdRig|RIG:neck_ctrl_end')
			headctrljnt[0].rename('head_ctrl_end')
			mmnamespace = self.getnamespace()
			bbox = pm.exactWorldBoundingBox(mmnamespace + 'body_hi')[4]
			headctrljnt[0].ty.set(bbox)
			pm.select(cl=True)

	def connectjoints(self, *args) :
		selection = pm.ls(os=True)
		lensel = len(selection)
		for idx, elem in enumerate(selection) :
			pm.connectJoint(selection[idx], selection[idx + 1], pm=True)
			#		print 'selection is -----> %s \n selection + 1 is -----> %s' %(selection[idx], selection [idx+1])
			if idx + 1 < lensel - 1 :
				idx += 1
			else :
				break

	def disconnectjoints(self) :
		jnt_1 = pm.ls(sl=True)
		jnt_2 = jnt_1[0].listRelatives(p=True)
		try :
			jnt_1[0].listRelatives(ap=True) != 0
			pm.disconnectJoint(jnt_1)
			pm.parent(jnt_1, 'crowdRig')
			pm.delete(jnt_2[0].listRelatives(c=True))
		except :
			print 'root joint can\'t be disconnected'