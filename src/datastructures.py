"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # This method generates a unique incremental ID
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        """
        Aqui añadimos un miembro nuevo a la familia.
        member tiene que ser un diccionario con:
        - first_name (string)
        - age (int > 0)
        - lucky_numbers (lista de ints)
        Opcional: id (int). Si no viene, lo generamos nosotros.
        last_name SIEMPRE será el de la familia (Jackson).
        """

        if not isinstance(member, dict):
            raise ValueError("Member must be a dict")

        first_name = member.get("first_name")
        age = member.get("age")
        lucky_numbers = member.get("lucky_numbers")

        # Hacemos validaciones para evitar basura
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name is required")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("age must be an int > 0")
        if not isinstance(lucky_numbers, list) or not all(isinstance(n, int) for n in lucky_numbers):
            raise ValueError("lucky_numbers must be a list of integers")

        # Usamos el id que nos dan si es valido y no se repite, sino generamos uno nuevo
        provided_id = member.get("id")
        if isinstance(provided_id, int):
            if any(m["id"] == provided_id for m in self._members):
                raise ValueError("id already exists")
            new_id = provided_id
        
            if provided_id >= self._next_id:
                self._next_id = provided_id + 1
        else:
            new_id = self._generate_id()

        new_member = {
            "id": new_id,
            "first_name": first_name.strip(),
            "last_name": self.last_name, 
            "age": age,
            "lucky_numbers": lucky_numbers
        }

        self._members.append(new_member)
        return new_member
        pass

    def delete_member(self, id):
        # borramos un miembro por id
        if not isinstance(id, int):
            raise ValueError("id debe ser int")

        for i, m in enumerate(self._members):
            if m["id"] == id:
                self._members.pop(i)
                return True

        return False
        pass

    def get_member(self, id):
        # buscamos un miembro por id y lo devolvemos
        if not isinstance(id, int):
            raise ValueError("id debe ser int")

        for m in self._members:
            if m["id"] == id:
                return m

        return None
        pass

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members