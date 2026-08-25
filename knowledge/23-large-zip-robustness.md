# Large ZIP robustness

ZIP-packning ska vara deterministisk och inkludera obligatoriska tomma kataloger.
Validera före extraction. Blockera duplicate/case-collision entries, traversal, symlinks, special files,
size/entry limits, extreme compression ratio och manifest mismatch.
